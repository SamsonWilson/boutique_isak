# mon_app/forms.py

from django import forms
from ..models import Utilisateur
# ... (gardez vos autres formulaires comme UtilisateurRegistrationForm et UtilisateurProfileForm)

# --- NOUVEAU FORMULAIRE pour la création par un admin avec mot de passe par défaut ---
class AdminUserCreationWithDefaultPasswordForm(forms.ModelForm):
    """
    Formulaire pour qu'un admin crée un utilisateur.
    Les champs de mot de passe sont volontairement omis.
    Le mot de passe sera défini dans la vue.
    """
    class Meta:
        model = Utilisateur
        # On inclut tous les champs SAUF le mot de passe.
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'boutique')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On peut rendre le champ 'boutique' obligatoire si un 'responsable' ou 'caissier' est créé.
        self.fields['boutique'].required = True
        self.fields['role'].required = True
        