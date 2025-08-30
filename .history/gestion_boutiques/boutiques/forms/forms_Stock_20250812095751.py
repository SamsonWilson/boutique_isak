from django import forms
from ..models import Stock

# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['boutique', 'produit', 'quantite']
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        # On inclut tous les champs que l'utilisateur doit remplir
        fields = ['boutique', 'produit', 'type_mouvement', 'quantite', 'description']

        widgets = {
            # Pour les listes déroulantes (ForeignKey, choices), Bootstrap 5 utilise 'form-select'
            'boutique': forms.Select(attrs={
                'class': 'form-select'
            }),
            'produit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'type_mouvement': forms.Select(attrs={
                'class': 'form-select'
            }),
            # Pour les champs de texte/nombre, on utilise 'form-control'
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantité à ajouter ou retirer',
                'min': '1' # Un mouvement a généralement une quantité > 0
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Raison du mouvement (optionnel)"
            })
        }

        labels = {
            'boutique': "Boutique concernée",
            'produit': "Produit",
            'type_mouvement': "Type de mouvement",
            'quantite': "Quantité",
            'description': "Description / Motif",
        }