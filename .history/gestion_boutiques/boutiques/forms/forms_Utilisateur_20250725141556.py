
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models import  Utilisateur


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