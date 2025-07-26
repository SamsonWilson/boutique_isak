# Dans votre fichier views.py

from django.views.generic.base import TemplateView
class AccueilView(TemplateView):
    # La seule chose à changer est cette ligne :
    template_name = "accueils/accueil.html" 