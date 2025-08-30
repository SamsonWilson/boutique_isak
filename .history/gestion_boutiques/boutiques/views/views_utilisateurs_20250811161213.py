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
    Vue basée sur les classes pour lister les utilisateurs,
    avec fonctionnalités de recherche, filtrage et pagination.
    """
    model = Utilisateur
    template_name = "utilisateurs/user_list.html"
    context_object_name = "utilisateurs"
    ordering = ['username']
    paginate_by = 15  # Ajout de la pagination : 15 utilisateurs par page

    def test_func(self):
        """La sécurité reste la même."""
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get_queryset(self):
        """
        Surcharge de la méthode pour filtrer les résultats en fonction
        des paramètres GET de l'URL (ex: ?q=test&role=caissier).
        """
        # On part du queryset de base (tous les utilisateurs)
        queryset = super().get_queryset()
        
        # On récupère les valeurs des filtres depuis l'URL
        search_query = self.request.GET.get('q')
        role_filter = self.request.GET.get('role')
        boutique_filter = self.request.GET.get('boutique')
        status_filter = self.request.GET.get('status')

        # Application du filtre de recherche textuelle
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        # Application du filtre par rôle
        if role_filter:
            queryset = queryset.filter(role=role_filter)
            
        # Application du filtre par boutique
        if boutique_filter:
            queryset = queryset.filter(boutique_id=boutique_filter)

        # Application du filtre par statut
        if status_filter:
            is_active = status_filter == 'true'
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Surcharge de la méthode pour ajouter au contexte :
        - Les données pour remplir les menus déroulants des filtres.
        - Les valeurs actuelles des filtres pour les "mémoriser" dans le formulaire.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestion des Utilisateurs"
        
        # Données pour les options des filtres
        context['role_choices'] = Utilisateur.ROLE_CHOICES
        context['boutiques'] = Boutique.objects.all().order_by('nom')
        
        # Mémorisation des filtres appliqués pour les réafficher dans le formulaire
        context['filter_values'] = self.request.GET
        
        return context

# Modification d’un utilisateur
class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = "utilisateurs/utilisateur_form.html"
    success_url = reverse_lazy("utilisateur_list")  # Redirection après modification