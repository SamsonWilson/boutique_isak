from django.views.generic.base import TemplateView

class AccueilView(TemplateView):
    template_name = "templates/accueil/accueil.html"