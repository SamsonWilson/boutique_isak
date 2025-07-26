# Dans votre fichier views.py

from django.views.generic.base import TemplateView
@method_decorator(login_required, name='dispatch')
class AccueilView(TemplateView):
    # La seule chose à changer est cette ligne :
    template_name = "accueils/accueil.html" 