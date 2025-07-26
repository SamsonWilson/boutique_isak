from django.views.generic.base import TemplateView

class AccueilView(TemplateView):
    template_name = "templates/accueils/accueil.html"