from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from ..models import Produit
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..forms.forms_produit import ProduitForm


class InventaireListView(ListView):
    model = Produit
    template_name = 'inventaire/inventaire.html'
    context_object_name = 'produits'


class Detail_venteListView(ListView):
    model = Produit
    template_name = 'inventaire/detail_de_vente.html'
    context_object_name = 'produits'
