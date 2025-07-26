from django.views.generic.base import TemplateView

class AccueilView(TemplateView):
    template_name = "template/accueil/accueil.html"