from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Pet, PetSitterProfile

def register_user(request):
    if request.method == "POST":
        # Common fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        # Basic validations
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Create Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create Profile
        profile = Profile.objects.create(
            user=user,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number=contact_number,
            address=address
        )

        # Role-based data
        if role == "sitter":
            bio = request.POST.get('bio')
            hourly_rate = request.POST.get('hourly_rate')
            availability = request.POST.get('availability')
            experience = request.POST.get('experience')

            PetSitterProfile.objects.create(
                sitter=user,
                bio=bio,
                hourly_rate=hourly_rate,
                availability=availability,
                experience_years=experience
            )
            return render(request, 'register.html', {"success_modal": "sitter"})

        elif role == "owner":
            pet_name = request.POST.get('pet_name')
            species = request.POST.get('species')
            breed = request.POST.get('breed')
            age = request.POST.get('age')

            Pet.objects.create(
                owner=user,
                pet_name=pet_name,
                species=species,
                breed=breed,
                age=age
            )
            return render(request, 'register.html', {"success_modal": "owner"})

        else:
            messages.error(request, "Invalid role selection.")
            return redirect('register')

    return render(request, 'register.html')
