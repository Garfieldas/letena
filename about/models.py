from django.db import models
import uuid

class About_us(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Pavadinimas')
    text = models.CharField(max_length=500, blank=False, verbose_name='Santrauka')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='Aktyvuoti')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tekstas"  # Single instance name
        verbose_name_plural = "Tekstai"


class Price_table(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Pavadinimas')
    combing1 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Šukavimas mažiem šunim')
    combing2 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Šukavimas dideliem šunim')
    showering1 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Plovimas mažiem šunim')
    showering2 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Plovimas dideliem šunim')
    drying1 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Sausinimas mažiem šunim')
    drying2 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Sausinimas dideliem šunim')
    consult1 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Konsultacija mažiem šunim')
    consult2 = models.IntegerField(blank=False, default=0, null=True, verbose_name='Konsultacija dideliem šunim')
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='Aktyvuoti')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslaugu kaina"  # Single instance name
        verbose_name_plural = "Paslaugu kainos"  # Plural name
