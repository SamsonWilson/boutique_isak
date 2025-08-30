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
    model = Utilisateur
    template_name = "utilisateurs/user_list.html"
    context_object_name = "utilisateurs"
    ordering = ['username']
    paginate_by = 15  # Optionnel mais recommandé : ajoute la pagination

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get_queryset(self):
        """
        Surcharge de la méthode pour filtrer les résultats.
        C'est ici que la magie opère.
        """
        # On récupère le queryset de base (tous les utilisateurs)
        queryset = super().get_queryset()
        
        # On récupère les paramètres de l'URL (ex: ?q=martin&role=caissier)
        search_query = self.request.GET.get('q', None)
        role_filter = self.request.GET.get('role', None)
        boutique_filter = self.request.GET.get('boutique', None)
        status_filter = self.request.GET.get('status', None)

        # 1. Filtre de recherche textuelle
        if search_query:
            # On cherche dans plusieurs champs en même temps
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        # 2. Filtre par rôle
        if role_filter:
            queryset = queryset.filter(role=role_filter)
            
        # 3. Filtre par boutique
        if boutique_filter:
            queryset = queryset.filter(boutique_id=boutique_filter)

        # 4. Filtre par statut
        if status_filter:
            if status_filter == 'true':
                queryset = queryset.filter(is_active=True)
            elif status_filter == 'false':
                queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute les données nécessaires aux filtres dans le contexte.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestion des Utilisateurs"
        
        # On passe les options pour les listes déroulantes du formulaire de filtre
        context['role_choices'] = Utilisateur.ROLE_CHOICES
        context['boutiques'] = Boutique.objects.all().order_by('nom')
        
        # On passe les valeurs actuelles des filtres pour les "mémoriser" dans le formulaire
        context['filter_values'] = self.request.GET
        
        return context

# Modification d’un utilisateur
class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = "utilisateurs/utilisateur_form.html"
    success_url = reverse_lazy("utilisateur_list")  # Redirection après modification