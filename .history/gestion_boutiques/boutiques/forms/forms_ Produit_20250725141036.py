
# --- Formulaire pour le modèle Produit ---
class ProduitForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un produit.
    """
    class Meta:
        model = Produit
        fields = '__all__'
        # Ou spécifiquement : fields = ['nom', 'description', 'prix_unitaire']
