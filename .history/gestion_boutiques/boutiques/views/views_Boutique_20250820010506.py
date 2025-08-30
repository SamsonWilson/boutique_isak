from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
# Create your views here.
from rest_framework import generics
from ..models import Boutique
from ..serializers.serializers_boutique import BoutiqueSerializer

class BoutiqueListCreateView(generics.ListCreateAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class BoutiqueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class BoutiqueListView(ListView):
    model = Boutique
    template_name = "boutique/liste.html"
    context_object_name = "boutiques"    