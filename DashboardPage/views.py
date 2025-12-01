from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import Profile
from .models import Notification
from django.http import JsonResponse
from django.utils import timezone

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    
    if profile.role == 'owner':
        return redirect('pet_owner_dashboard')
    elif profile.role == 'sitter':
        return redirect('pet_sitter_dashboard')
    
    return redirect('home')  
    
@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(owner=request.user).order_by('-created_at')

    data = []
    for n in notifications:
        created_at_local = timezone.localtime(n.created_at)
        data.append({
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": created_at_local.strftime("%b %d, %I:%M %p")
        })

    return JsonResponse({"notifications": data})
@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(owner=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"status": "success"})
