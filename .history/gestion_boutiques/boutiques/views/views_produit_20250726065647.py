from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Produit
from django.http import JsonResponse
from django.template.loader import render_to_string
from ..forms.forms_produit import ProduitForm

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
    success_url = 'produit_list'
    # success_url = ('produit_list')
     # Cette méthode est appelée quand une requête GET arrive
    def get(self, request, *args, **kwargs):
        # Si la requête est une requête AJAX, on renvoie uniquement le template partiel du formulaire
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # On change le template à utiliser pour cette requête spécifique
            self.template_name = 'votre_app/produit_form_partial.html'
        return super().get(request, *args, **kwargs)

    # Cette méthode est appelée quand le formulaire soumis est valide
    def form_valid(self, form):
        form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Pour AJAX, on renvoie une confirmation en JSON
            return JsonResponse({'success': True})
        # Pour une soumission normale, on suit la success_url
        return super().form_valid(form)

    # Cette méthode est appelée quand le formulaire soumis est invalide
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Pour AJAX, on renvoie le formulaire avec les erreurs en HTML
            form_html = render_to_string(
                'votre_app/produit_form_partial.html', 
                {'form': form}, 
                request=self.request
            )
            return JsonResponse({'success': False, 'form_html': form_html})
        # Pour une soumission normale, on ré-affiche la page avec les erreurs
        return super().form_invalid(form)

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produits/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')