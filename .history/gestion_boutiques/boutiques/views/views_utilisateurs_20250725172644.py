from django.contrib.auth.views import LoginView

class ConnexionView(LoginView):
    template_name = 'registration/loginconnexion.html'  # Ton template