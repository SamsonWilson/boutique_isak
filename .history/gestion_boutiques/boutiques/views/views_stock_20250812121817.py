from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Stock
from ..forms.forms_stock import StockForm


from django.contrib.auth.mixins import LoginRequiredMixin # L'équivalent de @login_required pour les CBV
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
    