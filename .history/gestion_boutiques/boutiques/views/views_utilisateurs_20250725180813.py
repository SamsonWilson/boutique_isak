from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class ConnexionView(LoginView):
    template_name = 'registration/login.html'  # Ton template
    success_url = reverse_lazy('accueil')