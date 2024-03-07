from django.db import models



# Create your models here.
from django.utils.text import slugify

class Offres(models.Model):
    libelle = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length=1000)
    prix = models.FloatField()
    image = models.ImageField(upload_to="uploads/", null=True)

    def save (self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.libelle)

        super().save(*args,**kwargs)

class Panier(models.Model):
    owner = models.CharField(max_length=100)
    libelle = models.CharField(max_length=50)
    item = models.IntegerField()
    prix = models.FloatField()
    slug = models.SlugField(blank=True)

    def save (self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.libelle)

        super().save(*args,**kwargs)

class Order(models.Model):
    owner = models.CharField(max_length=100)
    libelle = models.CharField(max_length=1000)
    item = models.IntegerField()
    prix = models.FloatField()
    slug = models.SlugField(blank=True)
    message = models.CharField(max_length=100,blank=True)
    PUBKEY = models.CharField(max_length=300,blank=True)
    QRCODE = models.CharField(max_length=300,blank=True)
    HEXA = models.CharField(max_length=3000,blank=True)

    def save (self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.libelle)
    
        super().save(*args,**kwargs)

class stat_vente(models.Model):
    libelle = models.CharField(max_length=300,primary_key=True)
    somme = models.IntegerField()
    
class Meta:
    managed = False
    db_table = 'utilisateur_stat_vente'