from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from ..models import MouvementStock,Boutique, Produit, StockCourant
from ..forms.forms_stock import MouvementStockForm,StockUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db import transaction

from django.contrib import messages
from django.utils.dateparse import parse_date

class StockListView(ListView):
    model = MouvementStock
    # template_name = 'produits/produit_list.html'
    # context_object_name = 'produits'
class StockCourantListView(ListView):
    model = StockCourant
    template_name = "stock/stock_courant_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        qs = StockCourant.objects.select_related("boutique", "produit")
        boutique_id = self.request.GET.get("boutique")
        if boutique_id:
            qs = qs.filter(boutique_id=boutique_id)
        return qs

class ProduitStockDetailView(ListView):
    model = MouvementStock
    template_name = "stocks/mouvement_list.html"
    context_object_name = "mouvements"
    paginate_by = 20  # optionnel, pour ne pas tout afficher sur une seule page

    def get_queryset(self):
        produit_id = self.kwargs["produit_id"]
        qs = MouvementStock.objects.filter(produit_id=produit_id).select_related("boutique", "produit", "utilisateur")

        # Trier par date ↓ (par défaut desc)
        qs = qs.order_by("-date_mouvement")

        # Filtre optionnel par date
        date_debut = self.request.GET.get("date_debut")
        date_fin = self.request.GET.get("date_fin")

        if date_debut:
            qs = qs.filter(date_mouvement__date__gte=parse_date(date_debut))
        if date_fin:
            qs = qs.filter(date_mouvement__date__lte=parse_date(date_fin))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produit_id = self.kwargs["produit_id"]
        context["produit"] = get_object_or_404(Produit, id=produit_id)
        return context
class StockCreateView(LoginRequiredMixin, CreateView):
    model = MouvementStock
    form_class = MouvementStockForm
    template_name = 'stocks/stock_form.html'
    success_url = reverse_lazy('produit_list')
    # model = MouvementStock
    # form_class = MouvementStockForm
    # template_name = 'stock/mouvement_form.html'
    # success_url = reverse_lazy('mouvement_list')

    @transaction.atomic
    def form_valid(self, form):
        # Associer l'utilisateur connecté
        form.instance.utilisateur = self.request.user
        response = super().form_valid(form)

        # Mettre à jour le stock
        mouvement = self.object
        stock, created = StockCourant.objects.get_or_create(
            boutique=mouvement.boutique,
            produit=mouvement.produit,
            defaults={'quantite': 0}
        )
        if mouvement.type_mouvement == 'entrée':
            stock.quantite += mouvement.quantite
        elif mouvement.type_mouvement == 'sortie':
            stock.quantite -= mouvement.quantite
        stock.save()
        return response
    # def get_context_data(self, **kwargs):
    #     """Ajoute des variables au contexte du template."""
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Ajouter un mouvement de stock'
    #     context['form_url'] = self.request.path
    #     return context

    # def form_valid(self, form):
    #     # On assigne l'utilisateur avant de décider quoi renvoyer
    #     form.instance.utilisateur = self.request.user
        
    #     # On sauvegarde le formulaire
    #     self.object = form.save()

    #     # On vérifie si la requête est une requête AJAX
    #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         return JsonResponse({'success': True})
    #     else:
    #         # Si ce n'est pas AJAX, on suit le comportement normal
    #         return super().form_valid(form)

    # def form_invalid(self, form):
    #     # Si la requête est AJAX et que le formulaire est invalide,
    #     # on renvoie le HTML du formulaire avec les erreurs.
    #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         context = self.get_context_data(form=form)
    #         return JsonResponse({
    #             'success': False,
    #             'form_html': render_to_string(self.template_name, context, request=self.request)
    #         })
    #     else:
    #         # Comportement normal pour une requête non-AJAX
    #         return super().form_invalid(form)

    # def form_invalid(self, form):
    #     if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         html = render_to_string(self.template_name, {'form': form}, request=self.request)
    #         return JsonResponse({'success': False, 'form_html': html})
    #     return super().form_invalid(form)

class StockUpdateView(LoginRequiredMixin,UpdateView):
    # model = MouvementStock
    model = StockCourant
    form_class = StockUpdateForm  # <-- On utilise notre formulaire personnalisé
    template_name = 'stocks/stock_Update_form.html'
    success_url = reverse_lazy('produit_list') # Assurez-vous que cette URL 'stock_list' existe
    def get_context_data(self, **kwargs):
        """
        On s'assure que le template reçoit bien l'objet sous le nom 'stock'.
        UpdateView le passe par défaut en tant que 'object' et 'stock'.
        """
        context = super().get_context_data(**kwargs)
        context['stock'] = self.object  # Le template utilise {{ stock.quantite }}
        return context
    @transaction.atomic
    def form_valid(self, form):
        stock_obj = self.object
        quantite_modif = form.cleaned_data.get('quantite_a_ajouter')
        description = form.cleaned_data.get('description')

        # Vérification sortie impossible si stock insuffisant
        if quantite_modif < 0 and stock_obj.quantite + quantite_modif < 0:
            messages.error(self.request, f"Stock insuffisant ({stock_obj.quantite} disponible).")
            return self.form_invalid(form)

        # 📌 Mise à jour du stock courant
        stock_obj.quantite += quantite_modif
        stock_obj.save()

        # 📌 Création d'une ligne dans l'historique
        MouvementStock.objects.create(
            boutique=stock_obj.boutique,
            produit=stock_obj.produit,
            quantite=abs(quantite_modif),
            type_mouvement='entrée' if quantite_modif > 0 else 'sortie',
            description=description,
            utilisateur=self.request.user if self.request.user.is_authenticated else None
        )

        messages.success(
            self.request,
            f"Le stock pour '{stock_obj.produit.nom}' a été modifié. Nouvelle quantité : {stock_obj.quantite}"
        )
        return super().form_valid(form)

    # def form_valid(self, form):
        # """
        # C'est ici que la magie opère. Cette méthode est appelée quand le formulaire est valide.
        # """
        # # On récupère la quantité saisie par l'utilisateur. On met 0 si le champ est vide.
        # quantite_ajoutee = form.cleaned_data.get('quantite_a_ajouter') or 0
        # if quantite_ajoutee != 0:
        #     # self.object est l'instance de Stock en cours de modification
        #     stock_actuel = self.object
        #     # On met à jour la quantité
        #     stock_actuel.quantite += quantite_ajoutee
        #     # On ajoute une sécurité pour ne pas avoir de stock négatif
        #     if stock_actuel.quantite < 0:
        #         stock_actuel.quantite = 0 # ou afficher une erreur
        #         messages.warning(self.request, "Le stock ne peut pas être négatif. Il a été remis à 0.")
        #     # On sauvegarde la modification en base de données
        #     stock_actuel.save()
        #     messages.success(self.request, f"Le stock pour '{stock_actuel.produit.nom}' a été mis à jour. Nouvelle quantité : {stock_actuel.quantite}")
        # else:
        #     messages.info(self.request, "Aucune modification de quantité n'a été effectuée.")
        # # On laisse la méthode parente gérer la redirection vers success_url
        # return super().form_valid(form)

# class StockUpdateView(UpdateView):
#     model = StockCourant
#     form_class = StockUpdateForm
#     template_name = 'stocks/stock_Update_form.html'
#     success_url = reverse_lazy('produit_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['stock'] = self.object
#         return context

#     @transaction.atomic
#     def form_valid(self, form):
#         stock_obj = self.object
#         quantite_modif = form.cleaned_data.get('quantite_a_modifier')
#         description = form.cleaned_data.get('description')

#         # Vérification sortie impossible si stock insuffisant
#         if quantite_modif < 0 and stock_obj.quantite + quantite_modif < 0:
#             messages.error(self.request, f"Stock insuffisant ({stock_obj.quantite} disponible).")
#             return self.form_invalid(form)

#         # 📌 Mise à jour du stock courant
#         stock_obj.quantite += quantite_modif
#         stock_obj.save()

#         # 📌 Création d'une ligne dans l'historique
#         MouvementStock.objects.create(
#             boutique=stock_obj.boutique,
#             produit=stock_obj.produit,
#             quantite=abs(quantite_modif),
#             type_mouvement='entrée' if quantite_modif > 0 else 'sortie',
#             description=description,
#             utilisateur=self.request.user if self.request.user.is_authenticated else None
#         )

#         messages.success(
#             self.request,
#             f"Le stock pour '{stock_obj.produit.nom}' a été modifié. Nouvelle quantité : {stock_obj.quantite}"
#         )
#         return super().form_valid(form)

class StockDeleteView(DeleteView):
    model = MouvementStock
    template_name = 'stock_confirm_delete.html'
    success_url = reverse_lazy('stock_list')



class StockDetailView(DetailView):
    model = MouvementStock
    template_name = 'stocks/Detail.html'  # Le template pour la modale
    context_object_name = 'stock'  # Un nom plus clair pour la liste dans le template

    # def get_queryset(self):
    #     """
    #     C'est ici qu'on filtre la liste des mouvements.
    #     Cette méthode retourne le queryset de base qui sera affiché.
    #     """
    #     # Récupère le queryset initial pour le produit/boutique concerné
    #     queryset = super().get_queryset().filter(
    #         boutique_id=self.kwargs['boutique_id'],
    #         produit_id=self.kwargs['produit_id']
    #     ).order_by('-date_mouvement')

    #     # Applique le filtre de date si le formulaire est soumis et valide
    #     self.form = DateRangeForm(self.request.GET)
    #     if self.form.is_valid():
    #         date_debut = self.form.cleaned_data.get('date_debut')
    #         date_fin = self.form.cleaned_data.get('date_fin')

    #         if date_debut:
    #             queryset = queryset.filter(date_mouvement__date__gte=date_debut)
    #         if date_fin:
    #             queryset = queryset.filter(date_mouvement__date__lte=date_fin)
        
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     """
    #     Ajoute des données supplémentaires au contexte pour le template.
    #     """
    #     context = super().get_context_data(**kwargs)
        
    #     # Ajoute les objets boutique et produit pour les afficher dans le titre de la modale
    #     context['boutique'] = get_object_or_404(Boutique, pk=self.kwargs['boutique_id'])
    #     context['produit'] = get_object_or_404(Produit, pk=self.kwargs['produit_id'])
        
    #     # Ajoute le formulaire de filtre au contexte
    #     context['form'] = self.form
        
    #     # Ajoute l'URL complète (avec les paramètres de filtre) pour l'action du formulaire
    #     context['form_url'] = self.request.get_full_path()
        
    #     return context

