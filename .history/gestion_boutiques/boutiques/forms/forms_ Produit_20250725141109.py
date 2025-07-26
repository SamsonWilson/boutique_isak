
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Boutique, Utilisateur, Produit, Stock, Vente, DetailVente


# --- Formulaire pour le modèle Produit ---
class ProduitForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un produit.
    """
    class Meta:
        model = Produit
        fields = '__all__'
        # Ou spécifiquement : fields = ['nom', 'description', 'prix_unitaire']