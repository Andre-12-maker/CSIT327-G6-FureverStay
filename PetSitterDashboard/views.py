from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import PetSitterProfile, Profile, SitterReview
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import SitterAvailability  
from PetOwnerDashboard.models import Booking
from django.views.decorators.http import require_GET
from datetime import datetime
from django.contrib.auth.models import User
from RegistrationPage.supabase_client import supabase

# --- Dashboard (View-only) ---
@login_required
def pet_sitter_dashboard(request):
    sitter = request.user  # current logged-in sitter

    # Get bookings related to this sitter
    sitter_reservations = Booking.objects.filter(
        sitter__sitter=sitter
    ).select_related('owner', 'sitter').prefetch_related('pets').order_by('-start_date')

    # Example: compute total earnings (optional)
    total_earnings = Booking.objects.filter(
        sitter__sitter=sitter, status='completed'
    ).aggregate(total=models.Sum('total_price'))['total'] or 0

    context = {
        'sitter_reservations': sitter_reservations,
        'total_earnings': total_earnings,
        'sitter_messages': [],  # placeholder until messages feature added
    }
    return render(request, 'pet_sitter_dashboard.html', context)


# --- Editable Profile Page ---
@login_required
def sitter_profile(request):
    sitter_profile, created = PetSitterProfile.objects.get_or_create(sitter=request.user)
    profile = Profile.objects.filter(user=request.user).first()
    reviews = SitterReview.objects.filter(sitter_id=request.user.id).select_related('reviewer').order_by('-created_at')
    avg_rating = reviews.aggregate(avg=models.Avg("rating"))["avg"] or 0
    avg_rating = round(avg_rating, 1)
    if request.method == "POST":
        sitter_profile.bio = request.POST.get("bio", "")
        sitter_profile.availability = request.POST.get("availability", "")
        sitter_profile.hourly_rate = request.POST.get("hourly_rate") or None
        sitter_profile.experience_years = request.POST.get("experience_years") or None

        # ---- Upload profile image to Supabase (override mode) ----
        if "profile_image" in request.FILES:
            file = request.FILES["profile_image"]

            # Always use the same filename to overwrite existing image
            path = f"sitter_profiles/{request.user.id}/profile.jpg"

            # Upload with upsert=True to override the file
            supabase.storage.from_("sitter_profiles").upload(
                path,
                file.read(),
                {"upsert": "true"}
            )

            # Get public URL
            url = supabase.storage.from_("sitter_profiles").get_public_url(path)
            sitter_profile.profile_image_url = url

        sitter_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("sitter_profile")

    context = {
        "sitter_profile": sitter_profile,
        "profile": profile,
        "reviews": reviews,
        "avg_rating": avg_rating,
    }
    return render(request, "pet_sitter_profile.html", context)



# ================================================================
# 📅 Availability API (for sitters to update their calendar)
# ================================================================
@csrf_exempt
@login_required
def update_availability(request):
    """
    POST endpoint to toggle sitter availability for a date.
    Example JSON body:
    { "date": "2025-10-31", "is_available": true }
    """
    if request.method == "POST":
        date_str = request.POST.get("date")
        is_available = request.POST.get("is_available") == "true"

        date_obj = parse_date(date_str)
        if not date_obj:
            return JsonResponse({"error": "Invalid date format."}, status=400)

        record, created = SitterAvailability.objects.get_or_create(
            sitter=request.user,
            date=date_obj,
            defaults={"is_available": is_available}
        )

        if not created:
            record.is_available = is_available
            record.save()

        return JsonResponse({
            "message": "Availability updated.",
            "date": date_obj.strftime("%Y-%m-%d"),
            "is_available": record.is_available
        })

    return JsonResponse({"error": "Invalid request method."}, status=405)


# ================================================================
# 📅 Fetch Availability for Logged-in Sitter (optional helper)
# ================================================================
@login_required
def get_availability(request):
    """
    GET endpoint: returns JSON of all dates & statuses for the logged-in sitter
    """
    records = SitterAvailability.objects.filter(sitter=request.user).values("date", "is_available")
    return JsonResponse(list(records), safe=False)


# ================================================================
# 📅 Fetch Availability for Pet Owner (public sitter profile)
# ================================================================
@require_GET
def fetch_sitter_availability(request, sitter_id):
    try:
        sitter = User.objects.get(id=sitter_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Sitter not found"}, status=404)

    month = request.GET.get("month")
    year = request.GET.get("year")

    availabilities = SitterAvailability.objects.filter(sitter=sitter)
    if month and year:
        availabilities = availabilities.filter(date__month=month, date__year=year)

    data = [
        {"date": str(a.date), "is_available": a.is_available}
        for a in availabilities
    ]

    # ✅ Return list directly
    return JsonResponse(data, safe=False)


# ================================================================
# 🧾 Booking Status Update (Accept/Decline)
# ================================================================
@login_required
def update_booking_status(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        try:
            booking = Booking.objects.get(id=booking_id)
            if booking.sitter.sitter == request.user:
                if action == "accept":
                    booking.status = "accepted"
                elif action == "decline":
                    booking.status = "declined"
                booking.save()
                return JsonResponse({"success": True, "status": booking.status})
            else:
                return JsonResponse({"success": False, "error": "Not authorized"})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
def complete_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")

        try:
            booking = Booking.objects.get(id=booking_id)

            # only sitter can complete their bookings
            if booking.sitter.sitter != request.user:
                return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

            booking.status = "completed"
            booking.save()

            return JsonResponse({"success": True, "status": "completed"})

        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def sitter_bookings(request):
    sitter = request.user

    reservations = Booking.objects.filter(
        sitter__sitter=sitter
    ).select_related("owner", "sitter").prefetch_related("pets").order_by("-start_date")

    return render(request, "bookings.html", {
        "sitter_reservations": reservations
    })
