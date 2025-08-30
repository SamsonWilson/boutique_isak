from django import forms


from ..models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix_unitaire']
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix_unitaire']
        
        # C'est ici que la magie opère !
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': "Entrez le nom du produit"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, # On peut définir la hauteur du champ de description
                'placeholder': "Décrivez le produit en quelques mots"
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Ex: 19.99"
            }),
        }
        
        # Bonus : On peut aussi personnaliser les labels et les textes d'aide
        labels = {
            'nom': "Nom du Produit",
            'prix_unitaire': "Prix unitaire (€)",
        }
        
        help_texts = {
            'description': "Cette description sera visible par les clients.",
        }        