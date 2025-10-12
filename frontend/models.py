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
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pet_name} ({self.species})"


# ------------------------------
# Signals
# Automatically create a Profile when a new User is created
# ------------------------------
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
