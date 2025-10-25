from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from RegistrationPage.models import Profile

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        # Authenticate user using email (used as username)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Get user's profile
            try:
                profile = Profile.objects.get(user=user)

                # Redirect based on role (use your actual model field name)
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


def logout_user(request):
    logout(request)
    return redirect('home')
