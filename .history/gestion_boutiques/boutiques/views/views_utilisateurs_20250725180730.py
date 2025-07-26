from django.contrib.auth.views import LoginView

class ConnexionView(LoginView):
    template_name = 'registration/login.html'  # Ton template
     success_url = reverse_lazy('vente_creer')