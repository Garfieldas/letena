from django.db import models
from django.contrib.auth.models import User
import uuid

class Appointment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True, verbose_name='Klientas')
    client_email = models.CharField(max_length=300, blank=False, verbose_name='El.paštas')
    client_phone = models.CharField(max_length=20, blank=False, verbose_name='Tel nr.')
    day = models.DateField(blank=False, verbose_name='Data')
    time = models.TimeField(blank=False, verbose_name='Laikas')
    is_completed = models.BooleanField(default=False, verbose_name='Įvykdytas')

    def __str__(self):
        return f"{self.day} - {self.time} - {self.client}"
    
    class Meta:
        verbose_name = "Vizitas"  # Single instance name
        verbose_name_plural = "Vizitai"  # Plural name

