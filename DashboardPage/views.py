from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from RegistrationPage.models import Profile, SitterReview
from .models import Notification
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

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

@login_required
def submit_review(request, sitter_id):
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        # Prevent users from reviewing themselves
        if request.user.id == sitter_id:
            messages.error(request, "You cannot review yourself.")
            return redirect('view_sitter_profile', sitter_id=sitter_id)

        # Create review
        SitterReview.objects.create(
            sitter_id=sitter_id,
            reviewer=request.user,
            rating=rating,
            comment=comment
        )
        sitter_user = Profile.objects.get(user_id=sitter_id).user
        Notification.objects.create(
            owner=sitter_user, 
            message=f"{request.user.first_name} left you a review: {rating} ⭐",
            type="review"
        )
        messages.success(request, "Your review has been submitted!")
        return redirect('view_sitter_profile', sitter_id=sitter_id)

    return redirect('view_sitter_profile', sitter_id=sitter_id)