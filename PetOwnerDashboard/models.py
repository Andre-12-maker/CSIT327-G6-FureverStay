from django.db import models
from django.contrib.auth.models import User
from RegistrationPage.models import PetSitterProfile, Pet

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    sitter = models.ForeignKey(PetSitterProfile, on_delete=models.CASCADE, related_name='bookings')
    pets = models.ManyToManyField(Pet, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    hours_per_day = models.PositiveIntegerField(default=1)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} → {self.sitter.profile.user.username} ({self.status})"
