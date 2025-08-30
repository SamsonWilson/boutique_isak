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
class StockUpdateForm(forms.ModelForm):
    """
    Ce formulaire est spécifiquement conçu pour la page de mise à jour du stock.
    Il ne contient qu'un seul champ, non lié au modèle, pour la quantité à ajouter.
    """
    quantite_a_ajouter = forms.IntegerField(
        label="Quantité à Ajouter / Retirer",
        required=False,  # Le champ n'est pas obligatoire
        initial=0,
        help_text="Utilisez un nombre positif pour ajouter, un nombre négatif pour retirer.",
        # widget=forms.NumberInput(attrs={'class': 'form-control' })
    )

    class Meta:
        model = Stock
        # La liste des champs est vide car nous ne voulons pas que Django
        # génère automatiquement des champs pour le modèle.
        # La mise à jour se fera manuellement dans la vue.
        fields = []