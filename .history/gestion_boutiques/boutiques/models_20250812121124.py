from django.db import models
from django.contrib.auth.models import AbstractUser

class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nom

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('responsable', 'Responsable boutique'),
        ('caissier', 'Caissier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    boutique = models.ForeignKey("Boutique", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.role})"
    
# class Categorie(models.Model):
#     nom = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="categories")

#     def __str__(self):
#         return self.nom


# class Fournisseur(models.Model):
#     nom = models.CharField(max_length=100)
#     contact = models.CharField(max_length=100, blank=True, null=True)
#     adresse = models.TextField(blank=True, null=True)
#     boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="fournisseurs")

#     def __str__(self):
#         return self.nom


# class Produit(models.Model):
#     nom = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     prix = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField(default=0)
#     code_barre = models.CharField(max_length=50, blank=True, null=True)
#     categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
#     fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
#     boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="produits")

#     def __str__(self):
#         return self.nom    
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

class Stock(models.Model):
    TYPE_CHOICES = [('entrée', 'Entrée'), ('sortie', 'Sortie')]
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0)
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_mouvement = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        unique_together = ('boutique', 'produit')
        def __str__(self):
            return self.uti

class Client(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="clients")
    def __str__(self):
        return self.nom
class Vente(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vente N°{self.id} - {self.date.strftime('%Y-%m-%d')}"

class DetailVente(models.Model):
    vente = models.ForeignKey(Vente, related_name='details', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)


# class PrixHistorique(models.Model):
#     produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
#     ancien_prix = models.DecimalField(max_digits=10, decimal_places=2)
#     nouveau_prix = models.DecimalField(max_digits=10, decimal_places=2)
#     date_changement = models.DateTimeField(auto_now_add=True)
#     utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
#     boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="historiques_prix")


class JournalAction(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    table_affectee = models.CharField(max_length=100)
    id_enregistrement = models.IntegerField()
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="journaux_actions")


class Inventaire(models.Model):
    date_inventaire = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="inventaires")

    def __str__(self):
        return f"Inventaire du {self.date_inventaire.strftime('%d/%m/%Y')}"

class InventaireDetail(models.Model):
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE, related_name="details")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    stock_theorique = models.IntegerField()
    stock_reel = models.IntegerField()
    ecart = models.IntegerField()

    def save(self, *args, **kwargs):
        # Calcul automatique de l'écart
        self.ecart = self.stock_reel - self.stock_theorique
        super().save(*args, **kwargs)

# class Achat(models.Model):
#     date_achat = models.DateTimeField(auto_now_add=True)
#     fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name="achats")

#     def __str__(self):
#         return f"Achat {self.id} - {self.date_achat}"


# class AchatDetail(models.Model):
#     achat = models.ForeignKey(Achat, on_delete=models.CASCADE, related_name="details")
#     produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
#     quantite = models.IntegerField()
#     prix_achat = models.DecimalField(max_digits=10, decimal_places=2)    