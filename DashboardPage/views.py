from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import Profile

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    
    if profile.role == 'owner':
        return redirect('pet_owner_dashboard')
    elif profile.role == 'sitter':
        return redirect('pet_sitter_dashboard')
    
    return redirect('home')  
