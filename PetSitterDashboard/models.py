from django.db import models
from django.contrib.auth.models import User

class SitterAvailability(models.Model):
    sitter = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('sitter', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.sitter.username} - {self.date} ({'Available' if self.is_available else 'Blocked'})"
