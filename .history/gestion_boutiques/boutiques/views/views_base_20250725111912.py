from django.views.generic.base import TemplateView

class AccueilView(TemplateView):
    template_name = "templats/accueil/accueil.html"