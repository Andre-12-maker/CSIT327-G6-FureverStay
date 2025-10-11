import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from frontend.models import Profile


# 🧠 Helper: Validate password strength
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


# 🧠 Helper: Generate unique username based on email prefix
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
    return redirect("home")


# 🐶 Register Pet Sitter
def register_pet_sitter(request):
    if request.method == "POST":
        return register_user(request, role="sitter")
    return redirect("home")


# 🔐 Universal Register Function
def register_user(request, role):
    name = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    confirm_password = request.POST.get("confirm_password", "").strip()

    # ✅ Validate name
    if not name or len(name) < 2:
        messages.error(request, "Name must be at least 2 characters.")
        return redirect("home")

    # ✅ Validate email
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Invalid email format.")
        return redirect("home")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return redirect("home")

    # ✅ Validate password
    if not is_valid_password(password):
        messages.error(
            request,
            "Password must be at least 8 characters, include uppercase, lowercase, number, and special character."
        )
        return redirect("home")

    if password != confirm_password:
        messages.error(request, "Passwords do not match.")
        return redirect("home")

    # ✅ Create user
    username = make_unique_username(email.split("@")[0])
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = name
    user.save()

    # ✅ Create profile with role
    Profile.objects.create(user=user, role=role)

    # ✅ Automatically login user
    login(request, user)

    # ✅ Redirect based on role
    if role == "owner":
        messages.success(request, "Registration successful! Welcome, Pet Owner 🐾")
        return redirect("pet_owner_dashboard")
    elif role == "sitter":
        messages.success(request, "Registration successful! Welcome, Pet Sitter 🐶")
        return redirect("pet_sitter_dashboard")

    # fallback
    return redirect("dashboard")


# 🔑 Login
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("loginEmail", "").strip()
        password = request.POST.get("loginPassword", "").strip()

        if not email or not password:
            messages.error(request, "Please fill in both email and password.")
            return redirect("home")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("home")

        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return redirect("home")

        login(request, user)

        # ✅ Redirect to correct dashboard
        if hasattr(user, "profile"):
            if user.profile.role == "owner":
                return redirect("pet_owner_dashboard")
            elif user.profile.role == "sitter":
                return redirect("pet_sitter_dashboard")
        return redirect("dashboard")

    return redirect("home")


# 🏡 Dashboards
@login_required(login_url='home')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url='home')
def pet_owner_dashboard(request):
    return render(request, "frontend/pet_owner_dashboard.html")


@login_required(login_url='home')
def pet_sitter_dashboard(request):
    return render(request, "frontend/pet_sitter_dashboard.html")


# 🚪 Logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("home")
