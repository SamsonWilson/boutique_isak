from django.db import models
from django.contrib.auth.models import AbstractUser

class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('responsable', 'Responsable boutique'),
        ('caissier', 'Caissier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    boutique = models.ForeignKey(Boutique, null=True, blank=True, on_delete=models.SET_NULL)

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

class Stock(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('boutique', 'produit')

class Vente(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vente N°{self.id} - {self.date.strftime('%Y-%m-%d')}"

class DetailVente(models.Model):
    vente = models.ForeignKey(Vente, related_name='details', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)