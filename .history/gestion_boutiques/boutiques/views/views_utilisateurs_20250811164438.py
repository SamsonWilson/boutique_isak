from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView, UpdateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from ..models import Utilisateur
from ..forms.forms_Utilisateur import AdminUserCreationWithDefaultPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
class ConnexionView(LoginView):
    template_name = 'registration/login.html'  # Ton template
    success_url = reverse_lazy('accueil')

class AdminUserCreateView(CreateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = 'Utilisateurs/utilisateur_form.html'
    success_url = reverse_lazy('liste_utilisateurs')  # à changer selon ta config

    def form_valid(self, form):
        # Définir un mot de passe par défaut
        default_password = "123456"  # tu peux mettre autre chose ou générer aléatoirement
        utilisateur = form.save(commit=False)
        utilisateur.password = make_password(default_password)
        utilisateur.save()

        messages.success(self.request, f"L'utilisateur {utilisateur.username} a été créé avec le mot de passe par défaut.")
        return super().form_valid(form)
# class UtilisateurListView(ListView):
#     model = Utilisateur
#     template_name = "utilisateurs/user_list.html"
#     context_object_name = "utilisateurs"
class UtilisateurListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue basée sur les classes pour lister les utilisateurs.
    Hérite de ListView pour afficher une liste d'objets.
    Hérite de LoginRequiredMixin pour s'assurer que l'utilisateur est connecté.
    Hérite de UserPassesTestMixin pour vérifier que l'utilisateur a le bon rôle.
    """
    model = Utilisateur  # Le modèle à utiliser
    template_name = "utilisateurs/user_list.html"  # Le chemin vers votre template
    context_object_name = "utilisateurs"  # Le nom de la variable dans le template
    ordering = ['username']  # Optionnel : pour trier les utilisateurs par nom d'utilisateur

    def test_func(self):
        """
        Cette fonction est requise par UserPassesTestMixin.
        Elle retourne True si l'utilisateur est autorisé, sinon False.
        """
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get_context_data(self, **kwargs):
        """
        Optionnel : pour ajouter des éléments supplémentaires au contexte.
        Ici, on ajoute un titre de page pour le rendre dynamique.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestion des Utilisateurs"
        return context
class ToggleUserStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue basée sur les classes pour activer/désactiver un utilisateur.
    Hérite de View car elle ne fait qu'exécuter une action et rediriger.
    """

    def test_func(self):
        """
        La même vérification de sécurité que pour la liste,
        pour s'assurer que seul un admin peut faire cette action.
        """
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def post(self, request, *args, **kwargs):
        """
        Cette méthode est appelée lorsqu'une requête POST est faite à l'URL.
        C'est ici que nous mettons toute la logique.
        """
        # On récupère le 'pk' de l'utilisateur depuis les arguments de l'URL
        user_pk = self.kwargs.get('pk')
        user_to_toggle = get_object_or_404(Utilisateur, pk=user_pk)
        
        # Sécurité : empêcher un admin de se désactiver lui-même
        if user_to_toggle == self.request.user:
            messages.error(self.request, "Vous ne pouvez pas désactiver votre propre compte.")
        else:
            # On inverse le statut
            user_to_toggle.is_active = not user_to_toggle.is_active
            user_to_toggle.save()
            
            # Message de confirmation
            status_text = "activé" if user_to_toggle.is_active else "désactivé"
            messages.success(self.request, f"L'utilisateur {user_to_toggle.username} a été {status_text}.")
        
        # On redirige vers la liste des utilisateurs
        return redirect('utilisateur_list')
        
    def get(self, request, *args, **kwargs):
        """
        Gère le cas où quelqu'un accède à l'URL via GET.
        On le redirige simplement, car aucune action ne doit être effectuée.
        """
        return redirect('utilisateur_list')
# Modification d’un utilisateur
class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = "utilisateurs/utilisateur_form.html"
    success_url = reverse_lazy("utilisateur_list")  # Redirection après modification