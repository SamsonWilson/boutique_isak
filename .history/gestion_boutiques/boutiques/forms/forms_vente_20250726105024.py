from django import forms
from django.forms import inlineformset_factory
from .models import Vente, DetailVente

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['boutique', 'utilisateur', 'total']  # 'total' en calcul ou input?

DetailVenteFormSet = inlineformset_factory(
    Vente,
    DetailVente,
    fields=('produit', 'quantite', 'prix_unitaire'),
    extra=1,         # nombre de lignes vides par défaut
    can_delete=True  # pour pouvoir retirer une ligne
)