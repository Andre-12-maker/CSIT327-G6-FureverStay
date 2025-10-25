from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import Profile, Pet, PetSitterProfile

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'owner':
        return redirect('pet_owner_dashboard')
    elif profile.role == 'sitter':
        return redirect('pet_sitter_dashboard')
    return render(request, 'dashboard.html')

@login_required
def pet_owner_dashboard(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_owner_dashboard.html', {'pets': pets})

@login_required
def pet_sitter_dashboard(request):
    sitter_profile = PetSitterProfile.objects.filter(sitter=request.user).first()
    return render(request, 'pet_sitter_dashboard.html', {'sitter_profile': sitter_profile})
