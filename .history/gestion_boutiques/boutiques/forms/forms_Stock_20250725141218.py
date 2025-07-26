
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Boutique, Utilisateur, Produit, Stock, Vente, DetailVente

# --- Formulaire pour le modèle Stock ---
class StockForm(forms.ModelForm):
    """
    Formulaire pour gérer le stock d'un produit dans une boutique.
    """
    class Meta:
        model = Stock
        fields = '__all__'
        # Ou spécifiquement : fields = ['boutique', 'produit', 'quantite']