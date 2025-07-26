from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Boutique, Utilisateur, Produit, Stock, Vente, DetailVente

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

# --- Formulaires pour le modèle Utilisateur (Custom User) ---
class UtilisateurCreationForm(UserCreationForm):
    """
    Formulaire pour la création d'un nouvel utilisateur.
    Hérite de UserCreationForm pour gérer la création et le hachage du mot de passe correctement.
    """
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        # On ajoute les champs personnalisés 'role' et 'boutique' au formulaire de création
        fields = UserCreationForm.Meta.fields + ('role', 'boutique', 'email', 'first_name', 'last_name')

class UtilisateurChangeForm(UserChangeForm):
    """
    Formulaire pour la modification d'un utilisateur existant dans l'interface d'administration.
    """
    class Meta(UserChangeForm.Meta):
        model = Utilisateur
        # Permet de modifier ces champs dans l'admin
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'boutique', 'is_active', 'is_staff', 'is_superuser')


# --- Formulaire pour le modèle Produit ---
class ProduitForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un produit.
    """
    class Meta:
        model = Produit
        fields = '__all__'
        # Ou spécifiquement : fields = ['nom', 'description', 'prix_unitaire']


# --- Formulaire pour le modèle Stock ---
class StockForm(forms.ModelForm):
    """
    Formulaire pour gérer le stock d'un produit dans une boutique.
    """
    class Meta:
        model = Stock
        fields = '__all__'
        # Ou spécifiquement : fields = ['boutique', 'produit', 'quantite']


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
