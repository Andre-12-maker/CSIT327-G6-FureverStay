from django.db import models
from django.contrib.auth.models import User

# ------------------------------
# Profile Model (Common for all users)
# ------------------------------
class Profile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Pet Owner'),
        ('sitter', 'Pet Sitter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Common details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ------------------------------
# Pet Model (For Pet Owners)
# ------------------------------
class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.pet_name} ({self.species})"


# ------------------------------
# Pet Sitter Profile Model
# ------------------------------
class PetSitterProfile(models.Model):
    sitter = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sitter_profile')
    bio = models.TextField(blank=True)
    availability = models.CharField(max_length=255, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='sitter_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.sitter.username}'s Sitter Profile"
