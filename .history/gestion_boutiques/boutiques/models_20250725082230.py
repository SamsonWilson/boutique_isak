from django.db import models

# Create your models here.
from django.db import models

class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=30)

    def __str__(self):
        return self.nom