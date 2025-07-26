from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Boutique
from .serializers import BoutiqueSerializer

class BoutiqueListCreateView(generics.ListCreateAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

class BoutiqueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer