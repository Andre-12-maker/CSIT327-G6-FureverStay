from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from RegistrationPage.models import Profile

# --- Password reset imports ---
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings


# ------------------------------
# LOGIN
# ------------------------------
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Get user's profile and redirect by role
            try:
                profile = Profile.objects.get(user=user)
                if profile.role == 'owner':
                    return redirect('pet_owner_dashboard')
                elif profile.role == 'sitter':
                    return redirect('pet_sitter_dashboard')
                else:
                    messages.error(request, "Invalid role assigned to this account.")
                    return redirect('login')
            except Profile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


# ------------------------------
# LOGOUT
# ------------------------------
def logout_user(request):
    logout(request)
    return redirect('home')


# ------------------------------
# PASSWORD RESET REQUEST
# ------------------------------
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect("password_reset_request")

        # Generate token & uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build reset URL
        reset_url = request.build_absolute_uri(f"/login/reset/{uid}/{token}/")

        # Send reset email
        subject = "Password Reset Request - FureverStay"
        message = (
            f"Hi {user.first_name} {user.last_name},\n\n"
            f"Click the link below to reset your password:\n{reset_url}\n\n"
            f"If you didn’t request this, please ignore this email."
        )

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(request, "Password reset link has been sent to your email.")
        return redirect("login")

    return render(request, "password_reset_request.html")


# ------------------------------
# PASSWORD RESET CONFIRM (set new password)
# ------------------------------
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "Invalid or expired reset link.")
        return redirect("password_reset_request")


# ------------------------------
# PASSWORD RESET COMPLETE
# ------------------------------
def password_reset_complete(request):
    return render(request, "password_reset_complete.html")
