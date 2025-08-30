from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Stock,Boutique, Produit
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
    template_name = 'stocks/Detail.html'  # Le template pour la modale
    context_object_name = '{% extends "base.html" %}
{% load static %}

{% block title %}Tableau de Bord - Gestion multi-boutiques{% endblock %}

{% block extra_head %}
    <!-- On charge le CSS et Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{% endblock %}

{% block content %}
<div class="modal-header">
    <h3>Historique pour : {{ produit.nom }}</h3>
    <p class="text-muted" style="margin:0;">Boutique : {{ boutique.nom }}</p>
</div>

<!-- Formulaire de filtre par date -->
<form method="GET" action="{{ form_url }}" id="date-filter-form" class="modal-form" style="display: flex; gap: 1rem; align-items: flex-end; margin-top: 1rem;">
    <div class="form-group" style="flex: 1;">
        {{ form.date_debut.label_tag }}
        {{ form.date_debut }}
    </div>
    <div class="form-group" style="flex: 1;">
        {{ form.date_fin.label_tag }}
        {{ form.date_fin }}
    </div>
    <button type="submit" class="btn btn-primary" style="margin-bottom: 1.2rem;">Filtrer</button>
</form>

<div class="table-wrapper" style="max-height: 350px;">
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Quantité</th>
                <th>Utilisateur</th>
            </tr>
        </thead>
        <tbody>
            {% for mvt in movements %}
                <tr>
                    <td>{{ mvt.date_mouvement|date:"d/m/Y H:i" }}</td>
                    <td>
                        {% if mvt.type_mouvement == 'entrée' %}
                            <span style="color: #38d39f;">● Entrée</span>
                        {% else %}
                            <span style="color: #e53e3e;">● Sortie</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if mvt.type_mouvement == 'entrée' %}+{% else %}-{% endif %}
                        {{ mvt.quantite }}
                    </td>
                    <td class="text-muted">{{ mvt.utilisateur.get_full_name|default:mvt.utilisateur.username }}</td>
                </tr>
            {% empty %}
                <tr>
                    <td colspan="4" style="text-align:center; padding: 20px;">
                        Aucun mouvement pour cette période.
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('main-modal');
    const modalBody = document.getElementById('modal-body');

    const openModal = (url) => {
        modal.style.display = 'block';
        modalBody.innerHTML = '<p style="text-align:center;">Chargement...</p>';

        fetch(url)
            .then(response => response.ok ? response.text() : Promise.reject('Erreur réseau.'))
            .then(html => {
                modalBody.innerHTML = html;
                
                const postForm = modalBody.querySelector('form[method="post"]');
                if (postForm) {
                    postForm.addEventListener('submit', handleFormSubmit);
                }
                
                const filterForm = modalBody.querySelector('#date-filter-form');
                if (filterForm) {
                    filterForm.addEventListener('submit', handleFilterSubmit);
                }
            })
            .catch(error => {
                modalBody.innerHTML = `<p style="color:red; text-align:center;">Erreur: Impossible de charger le contenu.</p>`;
                console.error('Erreur Fetch pour la modale:', error);
            });
    };

    const handleFilterSubmit = (event) => {
        event.preventDefault();
        const form = event.target;
        const url = new URL(form.action);
        url.search = new URLSearchParams(new FormData(form)).toString();
        openModal(url.href);
    };
});
</script>
{% endblock %}
'  # Un nom plus clair pour la liste dans le template

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

