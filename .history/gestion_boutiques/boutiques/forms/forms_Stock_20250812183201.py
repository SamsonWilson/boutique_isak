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

# forms.py
class DateRangeForm(forms.Form):
    date_debut = forms.DateField(
        label="Du",
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_fin = forms.DateField(
        label="Au",
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )        


# votre_app/forms.py
from django import forms
from .models import Stock # Assurez-vous d'importer votre modèle

class StockUpdateForm(forms.ModelForm):
    # === VÉRIFIEZ QUE CETTE DÉCLARATION EXISTE ET EST CORRECTE ===
    quantite_a_ajouter = forms.IntegerField(
        label="Quantité à ajouter / Retirer",
        required=False,  # Important pour ne pas forcer une modification
        initial=0,
        help_text="Utilisez un nombre positif pour ajouter, un nombre négatif pour retirer.",
        # On ajoute la classe CSS pour que Bootstrap l'affiche correctement
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # ==========================================================

    class Meta:
        model = Stock
        # La liste 'fields' doit être VIDE ou ne PAS contenir 'quantite'.
        # Elle sert à lier les champs du formulaire au modèle.
        # Comme 'quantite_a_ajouter' n'est pas dans le modèle, on ne le met pas ici.
        fields = [] # Vous pouvez lister ici d'autres champs du modèle à modifier (ex: ['emplacement'])    