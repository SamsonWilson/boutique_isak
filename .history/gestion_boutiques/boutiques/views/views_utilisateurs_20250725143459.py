# mon_app/views.py

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages  # <-- IMPORT MESSAGES

# Importer le nouveau formulaire
from .forms import AdminUserCreationWithDefaultPasswordForm, UtilisateurRegistrationForm, UtilisateurProfileForm
from .models import Utilisateur

# --- Vue de création par un admin (MISE À JOUR) ---

class AdminUserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Utilisateur
    # Utiliser notre nouveau formulaire sans champ de mot de passe
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = 'registration/admin_create_user.html'
    success_url = reverse_lazy('admin_create_user') # Rediriger vers la même page pour créer un autre user

    def test_func(self):
        """ Le test de permission ne change pas. """
        return self.request.user.is_superuser

    def form_valid(self, form):
        """
        Cette méthode est appelée lorsque les données du formulaire sont valides.
        C'est ici que nous allons définir le mot de passe par défaut.
        """
        # 1. Définir le mot de passe par défaut
        default_password = 'password123'  # AVERTISSEMENT : Changez ceci pour quelque chose de plus sécurisé !
                                          # Idéalement, générez un mot de passe aléatoire.

        # 2. Sauvegarder l'objet utilisateur SANS le commit dans la base de données
        user = form.save(commit=False)

        # 3. Définir le mot de passe haché
        user.set_password(default_password)

        # 4. Maintenant, sauvegarder l'utilisateur complet dans la base de données
        user.save()

        # 5. Créer un message de succès pour informer l'admin du mot de passe
        messages.success(
            self.request,
            f"L'utilisateur '{user.username}' a été créé avec succès. "
            f"Le mot de passe par défaut est : {default_password}. "
            f"Veuillez le communiquer à l'utilisateur de manière sécurisée."
        )

        # La méthode parente s'occupera de la redirection vers success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Créer un compte pour un employé"
        return context

# --- Les autres vues (UserRegisterView, ProfileUpdateView) ne changent pas ---