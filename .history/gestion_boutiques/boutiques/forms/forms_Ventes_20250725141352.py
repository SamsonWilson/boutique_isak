from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Boutique, Utilisateur, Produit, Stock, Vente, DetailVente

# --- Formulaire pour le modèle Boutique ---
# --- Formulaires pour les Ventes (Cas plus complexe) ---

class VenteForm(forms.ModelForm):
    """
    ATTENTION : Ce formulaire est rarement utilisé tel quel.
    En général, l'objet Vente est créé dans la vue (view) après la validation
    des détails de la vente. Le total, la date et l'utilisateur sont définis
    automatiquement, pas par l'utilisateur.
    """
    class Meta:
        model = Vente
        # On exclut les champs qui sont calculés ou définis automatiquement
        exclude = ['date', 'total', 'utilisateur']
        # On pourrait le lier à une boutique si nécessaire
        # fields = ['boutique'] 


class DetailVenteForm(forms.ModelForm):
    """
    Formulaire pour une seule ligne de détail dans une vente.
    Ce formulaire est destiné à être utilisé dans un "formset" (un ensemble de formulaires)
    pour permettre d'ajouter plusieurs produits à une seule vente.
    """
    class Meta:
        model = DetailVente
        # L'utilisateur ne choisira que le produit et la quantité.
        # Le 'prix_unitaire' sera copié depuis le produit et la 'vente' sera liée dans la vue.
        fields = ['produit', 'quantite']
