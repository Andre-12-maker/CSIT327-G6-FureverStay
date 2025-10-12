import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from frontend.models import Profile, Pet


# 🧠 Helper: Validate password
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[\W_]", password):
        return False
    return True


# 🧠 Helper: Generate unique username
def make_unique_username(base_username):
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username


# 🏠 Home Page
def home(request):
    return render(request, "home.html")


# 🐾 Register Pet Owner
def register_pet_owner(request):
    if request.method == "POST":
        return register_user(request, role="owner")
    return redirect("frontend:home")


# 🐶 Register Pet Sitter
def register_pet_sitter(request):
    if request.method == "POST":
        return register_user(request, role="sitter")
    return redirect("frontend:home")


# 🔐 Universal Register Function
def register_user(request, role):
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    confirm_password = request.POST.get("confirm_password", "").strip()

    # --- Validate names ---
    if not first_name or len(first_name) < 2:
        messages.error(request, "First name must be at least 2 characters.")
        return redirect("frontend:home")
    if not last_name or len(last_name) < 2:
        messages.error(request, "Last name must be at least 2 characters.")
        return redirect("frontend:home")

    # --- Validate email ---
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Invalid email format.")
        return redirect("frontend:home")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return redirect("frontend:home")

    # --- Validate password ---
    if not is_valid_password(password):
        messages.error(
            request,
            "Password must be at least 8 characters, include uppercase, lowercase, number, and special character."
        )
        return redirect("frontend:home")

    if password != confirm_password:
        messages.error(request, "Passwords do not match.")
        return redirect("frontend:home")

    # --- Create user ---
    base_username = email.split("@")[0]
    username = make_unique_username(base_username)
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # --- Create profile ---
    profile, created = Profile.objects.get_or_create(user=user, defaults={'role': role})
    if created:
        print(f"Profile created for {user.username} with role {role}")
    else:
        print(f"Profile already exists for {user.username}, role: {profile.role}")

    # --- Save pet info if owner ---
    if role == "owner":
        pet_name = request.POST.get("pet_name", "").strip()
        species = request.POST.get("species", "").strip()
        breed = request.POST.get("breed", "").strip()
        age = request.POST.get("age", "").strip()
        weight = request.POST.get("weight", "").strip()

        if pet_name and species and breed and age and weight:
            Pet.objects.create(
                owner=user,
                pet_name=pet_name,
                species=species,
                breed=breed,
                age=int(age),
                weight=float(weight)
            )
            print(f"Pet {pet_name} saved for owner {user.username}")
        else:
            print(f"Pet info incomplete for owner {user.username}")

    # --- Automatically login ---
    login(request, user)
    print("User logged in:", user.username)
    print("Profile exists:", hasattr(user, "profile"))
    if hasattr(user, "profile"):
        print("Role:", user.profile.role)

    # --- Redirect to appropriate dashboard ---
    try:
        profile_role = user.profile.role
        if profile_role == "owner":
            return redirect("frontend:pet_owner_dashboard")
        elif profile_role == "sitter":
            return redirect("frontend:pet_sitter_dashboard")
        else:
            print("Unknown role:", profile_role)
    except AttributeError:
        messages.warning(request, "Profile not found. Redirecting to home.")
        print("Profile missing for user:", user.username)

    return redirect("frontend:home")


# 🔑 Login
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("loginEmail", "").strip()
        password = request.POST.get("loginPassword", "").strip()

        if not email or not password:
            messages.error(request, "Please fill in both email and password.")
            return redirect("frontend:home")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("frontend:home")

        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return redirect("frontend:home")

        login(request, user)

        # --- Debug prints ---
        print("User logged in:", user.username)
        print("Profile exists:", hasattr(user, "profile"))
        if hasattr(user, "profile"):
            print("Role:", user.profile.role)

        try:
            profile_role = user.profile.role
            if profile_role == "owner":
                return redirect("frontend:pet_owner_dashboard")
            elif profile_role == "sitter":
                return redirect("frontend:pet_sitter_dashboard")
        except AttributeError:
            messages.warning(request, "No profile found for this user.")

        return redirect("frontend:home")

    return redirect("frontend:home")


# 🏡 Dashboards
@login_required(login_url='frontend:home')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='frontend:home')
def pet_owner_dashboard(request):
    return render(request, "frontend/pet_owner_dashboard.html")


@login_required(login_url='frontend:home')
def pet_sitter_dashboard(request):
    return render(request, "frontend/pet_sitter_dashboard.html")


# 🚪 Logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("frontend:home")
