from django.contrib.auth.views import LoginView

class ConnexionView(LoginView):
    template_name = 'connexion.html'  # Ton template