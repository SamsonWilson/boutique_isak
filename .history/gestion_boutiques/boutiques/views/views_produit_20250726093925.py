from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,
from ..models import Produit
from django.http import JsonResponse
from django.template.loader import render_to_string
from ..models import Produit
from ..forms.forms_produit import ProduitForm


# class ProduitListView(ListView):
#     model = Produit
#     template_name = 'produits/produit_list.html'
#     context_object_name = 'produits'
class DashboardView(TemplateView):
    template_name = 'votre_template_dashboard.html'

    def get_context_data(self, **kwargs):
        # 1. Récupérer le contexte de base
        context = super().get_context_data(**kwargs)
        
        # 2. Ajouter toutes les données dont on a besoin
        context['produits'] = Produit.objects.all()
        context['stocks'] = Stock.objects.all()
        
        # 3. Retourner le contexte complet
        return context
class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'produits/produit_detail.html'
    context_object_name = 'produit'

class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = 'produit_list'
    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'form_html': html})
        return super().form_invalid(form)
    # success_url = ('produit_list')
    

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produits/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')