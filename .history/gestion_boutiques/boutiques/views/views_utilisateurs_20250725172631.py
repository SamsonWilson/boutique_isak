from django.contrib.auth.views import LoginView

class ConnexionView(LoginView):
    template_name = 'registconnexion.html'  # Ton template