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
Use code with caution.
Python
Explication de chaque formulaire
BoutiqueForm:
Rôle : Créer ou mettre à jour une Boutique.
Champs : nom et adresse. Très simple et direct.
UtilisateurCreationForm & UtilisateurChangeForm:
Rôle : Gérer votre modèle Utilisateur personnalisé. Il est crucial d'hériter des formulaires de base de Django (UserCreationForm, UserChangeForm) car ils gèrent des aspects de sécurité importants, comme le hachage sécurisé des mots de passe.
UtilisateurCreationForm : Utilisé pour la page d'inscription. Il ajoute vos champs personnalisés (role, boutique) au formulaire de base.
UtilisateurChangeForm : Utilisé principalement dans l'interface d'administration de Django pour modifier les informations d'un utilisateur.
ProduitForm:
Rôle : Créer ou mettre à jour un Produit.
Champs : nom, description, et prix_unitaire.
StockForm:
Rôle : Ajouter un produit au stock d'une boutique ou mettre à jour la quantité.
Champs : L'utilisateur sélectionnera une boutique et un produit (via des listes déroulantes) et entrera une quantite. La contrainte unique_together de votre modèle empêchera de créer une entrée en double pour le même produit dans la même boutique.
VenteForm:
Rôle : C'est un cas particulier. Vous n'aurez probablement pas de page où un utilisateur remplit ce formulaire.
Pourquoi ? Une Vente est le résultat d'une transaction. L'objet Vente est créé automatiquement dans votre code (dans views.py) une fois que le caissier a terminé d'ajouter des produits.
date est auto_now_add=True.
utilisateur est l'utilisateur actuellement connecté.
total est la somme calculée de tous les DetailVente.
J'ai inclus un formulaire minimaliste pour montrer à quoi il ressemblerait, mais en pratique, il est rarement utilisé directement.
DetailVenteForm:
Rôle : C'est le formulaire clé pour enregistrer une vente. Il représente une seule ligne sur un ticket de caisse (par ex: "3 x Tomates à 1.50€").
Utilisation : Vous n'utiliserez pas ce formulaire seul. Vous utiliserez une formset_factory ou une inlineformset_factory de Django. Cela vous permet d'afficher plusieurs DetailVenteForm sur la même page, afin qu'un caissier puisse ajouter dynamiquement plusieurs produits à une même vente.
J'espère que cela vous aide à démarrer ! Le concept de formset pour les ventes est l'étape suivante la plus logique à explorer.