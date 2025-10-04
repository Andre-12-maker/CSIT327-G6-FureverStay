from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import random

# OTP storage for demo (not persistent)
OTP_STORAGE = {}

def home(request):
    if request.method == "POST":
        if "login" in request.POST:
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            if not username or not password:
                messages.error(request, "Please fill in both username and password.")
                return redirect("home")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials.")
                return redirect("home")

        elif "register_owner" in request.POST:
            username = request.POST.get("ownerUsername", "").strip()
            email = request.POST.get("ownerEmail", "").strip()
            password = request.POST.get("ownerPassword", "").strip()
            pet_name = request.POST.get("ownerPetName", "").strip()

            if not username or not email or not password or not pet_name:
                messages.error(request, "All fields are required for registration.")
                return redirect("home")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("home")

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Pet Owner registered successfully.")
            return redirect("home")

        elif "register_sitter" in request.POST:
            username = request.POST.get("sitterUsername", "").strip()
            email = request.POST.get("sitterEmail", "").strip()
            password = request.POST.get("sitterPassword", "").strip()
            experience = request.POST.get("sitterExperience", "").strip()

            if not username or not email or not password or not experience:
                messages.error(request, "All fields are required for registration.")
                return redirect("home")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("home")

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Pet Sitter registered successfully.")
            return redirect("home")

    return render(request, "home.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Please enter your email.")
            return redirect("home")

        if User.objects.filter(email=email).exists():
            otp = random.randint(1000, 9999)
            OTP_STORAGE[email] = otp
            request.session['reset_email'] = email
            print(f"DEBUG: OTP for {email} is {otp}")
            messages.success(request, "OTP sent to your email (check console for demo).")
            return redirect("home")
        else:
            messages.error(request, "Email not found.")
            return redirect("home")


def verify_otp(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        entered_otp = request.POST.get("otp", "").strip()
        if not entered_otp:
            messages.error(request, "Please enter OTP.")
            return redirect("home")

        if str(OTP_STORAGE.get(email)) == entered_otp:
            request.session['otp_verified'] = True
            messages.success(request, "OTP verified. Please reset your password.")
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP.")
            return redirect("home")


def reset_password(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        if not request.session.get("otp_verified"):
            messages.error(request, "OTP verification required.")
            return redirect("home")

        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not password or not confirm_password:
            messages.error(request, "Please fill in both password fields.")
            return redirect("home")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("home")

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Password reset successfully.")
        return redirect("home")
