from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default="general")  
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username}: {self.message}"
