from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models import Boutique, Utilisateur, Produit, Stock, Vente, DetailVente

# --- Formulaire pour le modèle Boutique ---
class BoutiqueForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une boutique.
    """
    class Meta:
        model = Boutique
        # Inclut tous les champs du modèle Boutique
        fields = '__all__' 
        # Ou spécifiquement : fields = ['nom', 'adresse']