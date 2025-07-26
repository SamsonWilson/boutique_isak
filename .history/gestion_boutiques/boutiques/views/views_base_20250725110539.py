from django.views.generic.base import TemplateView

class AccueilView(TemplateView):
    template_name = "/accueil.html"