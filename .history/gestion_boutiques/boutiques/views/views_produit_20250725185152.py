from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Produit
ProduitForm
class ProduitListView(ListView):
    model = Produit
    template_name = 'produits/produit_list.html'
    context_object_name = 'produits'

class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'produits/produit_detail.html'
    context_object_name = 'produit'

class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produits/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')