from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Stock
from ..forms.forms_stock import StockForm,DateRangeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class StockListView(ListView):
    model = Stock
    template_name = 'produits/produit_list.html'
    context_object_name = 'produits'

class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stocks/stock_form.html'
    success_url = reverse_lazy('stock_list')
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
class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')
class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock_confirm_delete.html'
    success_url = reverse_lazy('stock_list')



class StockDetailView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'votre_app/stock_detail_modal.html'  # Le template pour la modale
    context_object_name = 'movements'  # Un nom plus clair pour la liste dans le template

    def get_queryset(self):
        """
        C'est ici qu'on filtre la liste des mouvements.
        Cette méthode retourne le queryset de base qui sera affiché.
        """
        # Récupère le queryset initial pour le produit/boutique concerné
        queryset = super().get_queryset().filter(
            boutique_id=self.kwargs['boutique_id'],
            produit_id=self.kwargs['produit_id']
        ).order_by('-date_mouvement')

        # Applique le filtre de date si le formulaire est soumis et valide
        self.form = DateRangeForm(self.request.GET)
        if self.form.is_valid():
            date_debut = self.form.cleaned_data.get('date_debut')
            date_fin = self.form.cleaned_data.get('date_fin')

            if date_debut:
                queryset = queryset.filter(date_mouvement__date__gte=date_debut)
            if date_fin:
                queryset = queryset.filter(date_mouvement__date__lte=date_fin)
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte pour le template.
        """
        context = super().get_context_data(**kwargs)
        
        # Ajoute les objets boutique et produit pour les afficher dans le titre de la modale
        context['boutique'] = get_object_or_404(Boutique, pk=self.kwargs['boutique_id'])
        context['produit'] = get_object_or_404(Produit, pk=self.kwargs['produit_id'])
        
        # Ajoute le formulaire de filtre au contexte
        context['form'] = self.form
        
        # Ajoute l'URL complète (avec les paramètres de filtre) pour l'action du formulaire
        context['form_url'] = self.request.get_full_path()
        
        return context

