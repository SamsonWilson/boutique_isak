from django import forms
from django.forms import inlineformset_factory
from ..models import Client, Vente, DetailVente

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['boutique', 'utilisateur', 'client', 'total']  # date auto
        widgets = {
class DetailVenteForm(forms.ModelForm):
    class Meta:
        model = DetailVente
        fields = ['produit', 'quantite', 'prix_unitaire']

DetailVenteFormSet = inlineformset_factory(
    Vente, DetailVente, form=DetailVenteForm, extra=1, can_delete=False
)