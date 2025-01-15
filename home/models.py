from django.db import models
import uuid

class Carousel(models.Model):
    name = models.CharField(max_length=200, blank=False, verbose_name='Pavadinimas')
    photo1 = models.ImageField(null=False, upload_to='carousel/', verbose_name='Pirma nuotrauka')
    textbox1 = models.CharField(max_length=200, blank=False, default='Su meilė ir kruopštumu', verbose_name='Pirmos nuotraukos tekstas')
    photo2 = models.ImageField(null=False, upload_to='carousel/', verbose_name='Antra nuotrauka')
    textbox2 = models.CharField(max_length=200, blank=False, null=True, default='Mūsų mylimiausi klientai', verbose_name='Antros nuotraukos tekstas')
    photo3 = models.ImageField(null=False, upload_to='carousel/', default='Kiekfiena diena kaip  šventė', verbose_name='Trečia nuotrauka')
    textbox3 = models.CharField(max_length=200, blank=False, null=True, default='Kiekvieną dieną kaip šventė', verbose_name='Trečios nuotraukos tekstas')
    photo4 = models.ImageField(null=False, upload_to='carousel/', verbose_name='Ketvirta nuotrauka')
    textbox4 = models.CharField(max_length=200, blank=False, null=True, default='Visi laukiami', verbose_name='Ketvirtos nuotraukos tekstas')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='Aktyvuoti')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Nuotraukų karusėlė"  # Single instance name
        verbose_name_plural = "Nuotraukų karusėlės"  # Plural name
    
class About(models.Model):
    name = models.CharField(max_length=200, blank=False, verbose_name='Pavadinimas')
    intro_text = models.CharField(max_length=200, blank=False, verbose_name='Trumpas tekstas')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='Aktyvuoti')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Santrauka"  # Single instance name
        verbose_name_plural = "Santraukos"  # Plural name

class Client(models.Model):
    name = models.CharField(max_length=200, blank=False, verbose_name='Pavadinimas')

    client_name1 = models.CharField(max_length=100, blank=False, verbose_name='Pirmas klientas')
    client_image1 = models.ImageField(null=False, upload_to='clients/', verbose_name='Pirma nuotrauka')
    client_intro1 = models.CharField(max_length=200, blank=False, verbose_name='Apie 1 klientą')

    client_name2 = models.CharField(max_length=100, blank=False, verbose_name='Antras klientas')
    client_image2 = models.ImageField(null=False, upload_to='clients/', verbose_name='Antra nuotrauka')
    client_intro2 = models.CharField(max_length=200, blank=False, verbose_name='Apie 2 klientą')

    client_name3 = models.CharField(max_length=100, blank=False, verbose_name='Trečias klientas')
    client_image3 = models.ImageField(null=False, upload_to='clients/', verbose_name='Trečia nuotrauka')
    client_intro3 = models.CharField(max_length=200, blank=False, verbose_name='Apie 3 klientą')

    client_name4 = models.CharField(max_length=100, blank=False, verbose_name='Ketvirtas klientas')
    client_image4 = models.ImageField(null=False, upload_to='clients/', verbose_name='Ketvirta nuotrauka')
    client_intro4 = models.CharField(max_length=200, blank=False, verbose_name='Apie 4 klientą')
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='Aktyvuoti')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Geriausi klientai"  # Single instance name
        verbose_name_plural = "Geriausių klientų skiltis"  # Plural name
    

