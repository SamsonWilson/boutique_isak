from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from ..models import Produit,Stock
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..forms.forms_produit import ProduitForm


class ProduitListView(ListView):
    model = Produit
    template_name = 'inventaire/produit_list.html'
    context_object_name = 'produits'
