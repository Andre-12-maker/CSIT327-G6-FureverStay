from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import Pet
from django.http import JsonResponse
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from RegistrationPage.models import Profile, PetSitterProfile
from django.contrib import messages
from datetime import datetime
from .models import Booking, SavedSitter
from django.contrib.auth.models import User
from DashboardPage.models import Notification

# ✅ Optional: import if you have availability model
from PetSitterDashboard.models import SitterAvailability  


# ✅ Fetch sitter availability (used in calendar)
def get_sitter_availability(request, sitter_id):
    availabilities = SitterAvailability.objects.filter(
        sitter_id=sitter_id,
        is_available=True
    ).values("date")
    return JsonResponse(list(availabilities), safe=False)


# ✅ Load .env for Supabase credentials
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ✅ Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ✅ Pet Owner Dashboard (main view)
@login_required
def pet_owner_dashboard(request):
    pets = Pet.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(owner=request.user).select_related('sitter', 'sitter__sitter').prefetch_related('pets').order_by('-created_at')
    return render(request, 'pet_owner_dashboard.html', {
        'pets': pets,
        'bookings': bookings,
    })


# ✅ Fetch all sitters (used for search/filter)
@login_required
def fetch_sitters(request):
    location = request.GET.get("location", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    availability = request.GET.get("availability", "").strip()

    # Fetch all sitters
    sitter_query = supabase.table("RegistrationPage_petsitterprofile").select("*").execute()
    sitters = sitter_query.data or []

    # Fetch all profiles
    profile_query = supabase.table("RegistrationPage_profile").select("*").execute()
    profiles = profile_query.data or []

    # Map user_id → profile
    profile_map = {p["user_id"]: p for p in profiles}

    # Convert min/max prices safely
    try:
        min_price_val = float(min_price) if min_price else None
    except ValueError:
        min_price_val = None

    try:
        max_price_val = float(max_price) if max_price else None
    except ValueError:
        max_price_val = None

    filtered = []

    for sitter in sitters:
        user_id = sitter.get("sitter_id")
        profile = profile_map.get(user_id)
        if not profile:
            continue

        # Filter by location
        addr = profile.get("address", "")
        if location and location.lower() not in addr.lower():
            continue

        # Filter by hourly rate
        rate = sitter.get("hourly_rate")
        if rate is not None:
            try:
                rate = float(rate)
            except ValueError:
                continue
        else:
            rate = 0

        if min_price_val is not None and rate < min_price_val:
            continue
        if max_price_val is not None and rate > max_price_val:
            continue

        # Filter by availability
        avail = sitter.get("availability", "").lower()
        if availability and availability.lower() not in avail:
            continue

        # Append sitter info
        filtered.append({
            "sitter_id": user_id,
            "first_name": profile.get("first_name"),
            "last_name": profile.get("last_name"),
            "email": profile.get("email"),
            "contact_number": profile.get("contact_number"),
            "address": addr,
            "bio": sitter.get("bio") or "No bio provided.",
            "availability": sitter.get("availability") or "Not specified",
            "hourly_rate": rate,
            "experience_years": sitter.get("experience_years") or 0,
            "profile_image_url": sitter.get("profile_image_url") or "/static/assets/default_profile.png",
        })

    return JsonResponse({"sitters": filtered})


# ✅ View a specific sitter’s profile
@login_required
def view_sitter_profile(request, sitter_id):
    """
    Displays the full profile of a sitter — including their basic info,
    sitter details, availability, and hourly rate.
    """
    profile_query = supabase.table("RegistrationPage_profile").select("*").eq("user_id", sitter_id).execute()
    if not profile_query.data:
        return render(request, "PetOwnerDashboard/view_sitter_profile.html", {"error": "Sitter not found."})

    profile = profile_query.data[0]

    sitter_profile_query = supabase.table("RegistrationPage_petsitterprofile").select("*").eq("sitter_id", profile["user_id"]).execute()
    sitter_profile = sitter_profile_query.data[0] if sitter_profile_query.data else None
    pets = Pet.objects.filter(owner=request.user)

    context = {
        "profile": profile,
        "sitter_profile": sitter_profile,
        "pets": pets,  
        "sitter_id": sitter_id,
    }

    return render(request, "view_sitter_profile.html", context)


@login_required
def create_booking(request, sitter_id):
    sitter = get_object_or_404(PetSitterProfile, sitter_id=sitter_id)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        hours_per_day = request.POST.get('hours_per_day')
        pet_ids = request.POST.getlist('pets')  # 🐾 multiple pet IDs from checkboxes

        # ✅ Validation
        if not pet_ids:
            messages.error(request, "Please select at least one pet for booking.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        if not start_date or not end_date or not hours_per_day:
            messages.error(request, "Please fill out all fields (dates, hours, pets).")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            hours_per_day = int(hours_per_day)
        except ValueError:
            messages.error(request, "Invalid input format.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        if end < start:
            messages.error(request, "End date cannot be before start date.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        if hours_per_day <= 0 or hours_per_day > 24:
            messages.error(request, "Hours per day must be between 1 and 24.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        # ✅ Fetch selected pets
        selected_pets = Pet.objects.filter(id__in=pet_ids, owner=request.user)
        num_pets = selected_pets.count()

        if num_pets == 0:
            messages.error(request, "Invalid pet selection.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        # ✅ Compute total cost (per pet)
        days = (end - start).days + 1
        total_price = days * hours_per_day * float(sitter.hourly_rate) * num_pets

        # ✅ Save booking
        booking = Booking.objects.create(
            owner=request.user,
            sitter=sitter,
            start_date=start,
            end_date=end,
            hours_per_day=hours_per_day,
            total_price=total_price,
        )
        booking.pets.set(selected_pets)
        # 🔔 Create notification for the pet owner
        Notification.objects.create(
            owner=request.user,
            message=f"Your booking request for {sitter.sitter.profile.first_name} has been sent.",
            type="booking"
        )
        # 🔔 Notify the sitter too (optional)
        Notification.objects.create(
            owner=sitter.sitter,  # the pet sitter user
            message=f"You received a new booking request from {request.user.first_name}.",
            type="booking"
        )
        messages.success(
            request,
            f"Booking sent to {sitter.sitter.profile.first_name}! ({num_pets} pets) Total ₱{total_price:.2f}"
        )
        return redirect('pet_owner_dashboard')

    return redirect('view_sitter_profile', sitter_id=sitter_id)

#Save / Remove Saved Sitter
@login_required
def save_sitter(request, sitter_id):
    sitter = User.objects.get(id=sitter_id)

    SavedSitter.objects.get_or_create(
        owner=request.user,
        sitter=sitter
    )

    return JsonResponse({"status": "saved"})

@login_required
def remove_saved_sitter(request, sitter_id):
    SavedSitter.objects.filter(
        owner=request.user,
        sitter_id=sitter_id
    ).delete()

    return JsonResponse({"status": "removed"})

@login_required
def get_saved_sitters(request):
    saved = SavedSitter.objects.filter(owner=request.user).select_related("sitter", "sitter__profile", "sitter__sitter_profile")

    sitter_list = []

    for s in saved:
        sitter_profile = getattr(s.sitter, "sitter_profile", None)
        profile = s.sitter.profile  

        sitter_list.append({
            "id": s.sitter.id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "address": profile.address,
            "hourly_rate": sitter_profile.hourly_rate if sitter_profile else None,
            "image": sitter_profile.profile_image_url if sitter_profile else "/static/assets/default_profile.png",
        })

    return JsonResponse({"saved": sitter_list})

@login_required
def pet_owner_profile(request):
    # Get or create the user's Profile
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={
        'role': 'owner',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    })

    # Get all pets for this owner
    pets = Pet.objects.filter(owner=request.user)

    if request.method == "POST":
        # Check if it's the "Add Pet" form
        if 'name' in request.POST:
            pet_name = request.POST.get("name")
            species = request.POST.get("pet_type")
            breed = request.POST.get("breed")
            age = request.POST.get("age") or 0

            Pet.objects.create(
                owner=request.user,
                pet_name=pet_name,
                species=species,
                breed=breed,
                age=age
            )
            Notification.objects.create(
                owner=request.user,
                message=f"You added a new pet: {pet_name}.",
                type="pet_added"
            )
            messages.success(request, f"{pet_name} added successfully!")
            return redirect("pet_owner_profile")
    context = {
        "profile": profile,
        "pets": pets,
    }

    return render(request, "pet_owner_profile.html", context)
