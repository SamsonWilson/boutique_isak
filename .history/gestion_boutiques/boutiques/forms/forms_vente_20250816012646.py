from django import forms
from django.forms import inlineformset_factory
from ..models import Client, Vente, DetailVente

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'contact', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone ou Email'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse'}),
        }

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['total']
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant total'}),
        }

DetailVenteFormSet = inlineformset_factory(
    Vente, DetailVente,
    fields=['produit', 'quantite', 'prix_unitaire'],
    extra=2, can_delete=True,
    widgets={
        'produit': forms.Select(attrs={'class': 'form-select'}),
        'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
        'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)