from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
# Create your views here.
from rest_framework import generics
from ..models import Boutique
from ..serializers.serializers_boutique import BoutiqueSerializer
from django.views.generic import ListView
from django.db.models import Q
from .models import Boutique
class BoutiqueListCreateView(generics.ListCreateAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class BoutiqueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class BoutiqueListView(ListView):
    model = Boutique
    template_name = "boutique/liste_boutique.html"
    context_object_name = "boutiques"   
    paginate_by = 5  # nombre d'éléments par page

    def get_queryset(self):
        qs = Boutique.objects.all().order_by("nom")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(nom__icontains=query) | Q(adresse__icontains=query)
            )
        return qs 