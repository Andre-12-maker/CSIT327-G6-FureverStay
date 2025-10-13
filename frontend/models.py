from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ------------------------------
# Profile Model
# ------------------------------
class Profile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Pet Owner'),
        ('sitter', 'Pet Sitter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ------------------------------
# Pet Model
# ------------------------------
class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.pet_name} ({self.species})"

#Pet Sitter Profile Model
class PetSitterProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True)
    availability = models.CharField(max_length=255, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    years_experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Sitter Profile"


