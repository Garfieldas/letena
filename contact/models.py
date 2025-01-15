from django.db import models
import uuid

class Review(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Vardas')
    service = models.CharField(max_length=100, blank=False, verbose_name='Paslauga')
    email = models.EmailField(max_length=200, blank=False, verbose_name='El.paštas')
    rate = models.TextField(blank=False, verbose_name='Apžvalga')
    is_active = models.BooleanField(default=True, verbose_name='Aktyvuoti')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Atsiliepimas"  # Single instance name
        verbose_name_plural = "Atsiliepimai"  # Plural name
    

class Message(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Vardas')
    email = models.EmailField(max_length=200, blank=False)
    phone = models.CharField(max_length=20, blank=False, verbose_name='Tel.nr')
    message = models.CharField(max_length=300, blank=False, verbose_name='Žinutė')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Parašymo data')
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Žinutė"  # Single instance name
        verbose_name_plural = "Žinutės"  # Plural name

