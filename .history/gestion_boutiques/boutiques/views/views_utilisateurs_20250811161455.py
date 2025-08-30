from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView, UpdateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from ..models import Utilisateur
from ..forms.forms_Utilisateur import AdminUserCreationWithDefaultPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

# Modification d’un utilisateur
class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = "utilisateurs/utilisateur_form.html"
    success_url = reverse_lazy("utilisateur_list")  # Redirection après modification