# Dans votre fichier views.py

from django.views.generic.base import TemplateView
class AccueilView(TemplateView):
    # La seule chose à changer est cette ligne :
    template_name = "accueils/accueil.html" 
    # Exemple dans une vue basée sur les classes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['utilisateur'] = self.request.user
        return context
