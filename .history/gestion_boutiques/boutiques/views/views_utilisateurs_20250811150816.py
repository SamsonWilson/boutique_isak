from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class ConnexionView(LoginView):
    template_name = 'registration/login.html'  # Ton template
    success_url = reverse_lazy('accueil')

class AdminUserCreateView(CreateView):
    model = Utilisateur
    form_class = AdminUserCreationWithDefaultPasswordForm
    template_name = 'utilisateur/admin_user_create.html'
    success_url = reverse_lazy('liste_utilisateurs')  # à changer selon ta config

    def form_valid(self, form):
        # Définir un mot de passe par défaut
        default_password = "123456"  # tu peux mettre autre chose ou générer aléatoirement
        utilisateur = form.save(commit=False)
        utilisateur.password = make_password(default_password)
        utilisateur.save()

        messages.success(self.request, f"L'utilisateur {utilisateur.username} a été créé avec le mot de passe par défaut.")
        return super().form_valid(form)