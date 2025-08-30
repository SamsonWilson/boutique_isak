from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from ..models import Produit,Stock
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..forms.forms_produit import ProduitForm
from django.db.models import Sum, Case, When, IntegerField



class ProduitListView(ListView):
    model = Produit
    template_name = 'produits/produit_list.html'
    context_object_name = 'produits'
    def get_dashboard_context():
        stock_summary = Stock.objects.values(
        'boutique__id', 
        'boutique__nom', 
        'produit__id', 
        'produit__nom'
    ).annotate(
        quantite_actuelle=Sum(
            Case(
                When(type_mouvement='entrée', then='quantite'),
                When(type_mouvement='sortie', then=-1 * F('quantite')), # Utiliser F() pour multiplier
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('boutique__nom', 'produit__nom')

        return {
        'produits': Produit.objects.all(),
        'stock_summary': stock_summary,
        # 'stocks' n'est plus nécessaire si on affiche le résumé
    }
class DashboardView(TemplateView):
    template_name = 'produits/produit_list.html'

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
    def get_context_data(self, **kwargs):
        """Ajoute des variables au contexte du template."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter un mouvement de stock'
        context['form_url'] = self.request.path
        return context

    def form_valid(self, form):
        # On assigne l'utilisateur avant de décider quoi renvoyer
        form.instance.utilisateur = self.request.user
        
        # On sauvegarde le formulaire
        self.object = form.save()

        # On vérifie si la requête est une requête AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            # Si ce n'est pas AJAX, on suit le comportement normal
            return super().form_valid(form)

    def form_invalid(self, form):
        # Si la requête est AJAX et que le formulaire est invalide,
        # on renvoie le HTML du formulaire avec les erreurs.
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data(form=form)
            return JsonResponse({
                'success': False,
                'form_html': render_to_string(self.template_name, context, request=self.request)
            })
        else:
            # Comportement normal pour une requête non-AJAX
            return super().form_invalid(form)

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