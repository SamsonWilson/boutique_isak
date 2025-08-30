from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from ..models import Produit, StockCourant, Vente, DetailVente
from ..forms.forms_vente import ClientForm, VenteForm, DetailVenteFormSet
# dans votre ventes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.http import JsonResponse
import json
from decimal import Decimal
from django.views import View
from django.contrib import messages
from django.views.generic import ListView

# class VenteCreateView(FormView):
#     template_name = 'ventes/vente_dashboard.html'
#     form_class = ClientForm
#     success_url = "/ventes/"

#     def form_valid(self, form):
#         items_json = self.request.POST.get("items")
#         if not items_json:
#             form.add_error(None, "⚠️ Aucun produit sélectionné.")
#             return self.form_invalid(form)

#         items = json.loads(items_json)

#         # Création client
#         client = form.save(commit=False)
#         client.boutique = self.request.user.boutique
#         client.save()

#         # Calcul du total
#         total = sum(Decimal(i["price"]) * int(i["quantity"]) for i in items)

#         # Sauvegarde Vente
#         vente = Vente.objects.create(
#             client=client,
#             boutique=self.request.user.boutique,
#             utilisateur=self.request.user,
#             total=total
#         )

#         # Détails
#         for i in items:
#             DetailVente.objects.create(
#                 vente=vente,
#                 produit_id=i["id"],
#                 quantite=int(i["quantity"]),
#                 prix_unitaire=Decimal(i["price"])
#             )

#         return redirect("vente_detail", pk=vente.pk)
class VenteCreateView(FormView):
    template_name = 'ventes/vente_dashboard.html'
    form_class = ClientForm
    success_url = reverse_lazy('vente_dashboard')

    def form_valid(self, form):
        items_json = self.request.POST.get("items")
        if not items_json:
            form.add_error(None, "⚠️ Aucun produit sélectionné.")
            return self.form_invalid(form)

        items = json.loads(items_json)

        # --- 1. Client ---
        client = form.save(commit=False)
        client.boutique = self.request.user.boutique
        client.save()

        # --- 2. Total ---
        total = sum(Decimal(str(i["price"])) * int(i["quantity"]) for i in items)

        # --- 3. Vente ---
        vente = Vente.objects.create(
            client=client,
            boutique=self.request.user.boutique,
            utilisateur=self.request.user,
            total=total
        )

        # --- 4. Détails + MAJ Stock ---
        for i in items:
            produit = Produit.objects.get(pk=i["id"])
            quantite = int(i["quantity"])
            prix_unitaire = Decimal(str(i["price"]))

            # Détail de la vente
            DetailVente.objects.create(
                vente=vente,
                produit=produit,
                quantite=quantite,
                prix_unitaire=prix_unitaire
            )

            # Mise à jour du stock courant
            try:
                stock = StockCourant.objects.get(produit=produit, boutique=self.request.user.boutique)
                if stock.quantite >= quantite:
                    stock.quantite -= quantite
                    stock.save()
                else:
                    form.add_error(None, f"⚠️ Stock insuffisant pour {produit.nom} (dispo: {stock.quantite})")
                    # Supprimer la vente incomplète si nécessaire
                    vente.delete()
                    return self.form_invalid(form)
            except StockCourant.DoesNotExist:
                form.add_error(None, f"⚠️ Aucun stock courant pour {produit.nom}")
                vente.delete()
                return self.form_invalid(form)
        # # Feedback utilisateur
        # messages.success(self.request, f"✅ Vente N°{vente.pk} enregistrée, stock mis à jour.")
        messages.success(self.request, "✅ Vente enregistrée avec succès")
        # On redirige vers PDF (voir CBV ci-dessous)
        return redirect("vente_pdf", pk=vente.pk)
        # return super().form_valid(form)
        # return redirect("vente_detail", pk=vente.pk)
# 🔎 API Ajax pour rechercher les produits

# views.py


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()

        produits = StockCourant.objects.filter(
            produit__nom__icontains=q
        ).select_related('produit')[:10]

        data = [
            {
                "id": p.produit.id,                         # identifiant du produit
                "name": p.produit.nom,                      # nom du produit
                "price": float(p.produit.prix_unitaire),    # prix unitaire
                "quantityStock": p.quantite                 # stock dispo
            }
            for p in produits
        ]

        return JsonResponse(data, safe=False)
# views.py


class VenteListView(ListView):
    model = Vente
    template_name = "ventes/ventes.html"
    context_object_name = "ventes"

    def get_queryset(self):
        # On utilise select_related et prefetch_related pour optimiser les requêtes
        return (
            Vente.objects
            .select_related("client", "boutique", "utilisateur")
            .prefetch_related("details__produit")
        )
# class VenteCreateView(View):
#     template_name = 'ventes/vente_dashboard.html'

#     def get(self, request):
#         client_form = ClientForm()
#         vente_form = VenteForm()
#         formset = DetailVenteFormSet()
#         return render(request, self.template_name, {
#             'client_form': client_form,
#             'vente_form': vente_form,
#             'formset': formset
#         })

#     def post(self, request):
#         client_form = ClientForm(request.POST)
#         vente_form = VenteForm(request.POST)
#         formset = DetailVenteFormSet(request.POST)
#         if client_form.is_valid() and vente_form.is_valid():
#             client = client_form.save()
#             vente = vente_form.save(commit=False)
#             vente.client = client  # Associe le client à la vente
#             vente.save()
#             formset = DetailVenteFormSet(request.POST, instance=vente)
#             if formset.is_valid():
#                 formset.save()
#                 return redirect('success_page')  # À adapter
#         # Si erreur, on affiche les formulaires avec les erreurs
#         return render(request, self.template_name, {
#             'client_form': client_form,
#             'vente_form': vente_form,
#             'formset': formset
#         })
# class VenteCreateView(View):
#     template_name = 'ventes/vente_dashboard.html'

#     def get(self, request):
#         vente_form = VenteForm()
#         detail_formset = DetailVenteFormSet()
#         ventes = Vente.objects.prefetch_related('details', 'details__produit')
#         return render(request, self.template_name, {
#             'vente_form': vente_form,
#             'detail_formset': detail_formset,
#             'ventes': ventes,
#         })
    
#     def post(self, request):
#         vente_form = VenteForm(request.POST)
#         detail_formset = DetailVenteFormSet(request.POST)

#         if vente_form.is_valid() and detail_formset.is_valid():
#             vente = vente_form.save()
#             details = detail_formset.save(commit=False)
#             total = 0
#             for detail in details:
#                 detail.vente = vente
#                 detail.save()
#                 total += detail.prix_unitaire * detail.quantite
#             vente.total = total
#             vente.save()
#             return redirect('vente_dashboard')  # adapte à ton url name
        
#         ventes = Vente.objects.prefetch_related('details', 'details__produit')
#         return render(request, self.template_name, {
#             'vente_form': vente_form,
#             'detail_formset': detail_formset,
#             'ventes': ventes,
#         })
# from django.views.generic import FormView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.shortcuts import redirect
# from django.utils import timezone
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from ..models import Vente, DetailVente, Stock
# from ..forms.forms_vente import VenteForm

# class VenteCreateView(LoginRequiredMixin, FormView):
#     template_name = 'core/vente_form.html'
#     form_class = VenteForm
#     success_url = reverse_lazy('vente_creer')

#     def form_valid(self, form):
#         produits = form.cleaned_data['produits']
#         quantites = form.cleaned_data['quantites_list']
#         utilisateur = self.request.user
#         boutique = utilisateur.boutique

#         if not boutique:
#             messages.error(self.request, "Vous n'avez pas de boutique assignée.")
#             return redirect('vente_creer')

#         total = 0
#         # Vérification des stocks
#         for produit, qte in zip(produits, quantites):
#             try:
#                 stock = Stock.objects.get(boutique=boutique, produit=produit)
#                 if stock.quantite < qte:
#                     messages.error(self.request, f"Stock insuffisant pour {produit.nom}.")
#                     return self.form_invalid(form)
#             except Stock.DoesNotExist:
#                 messages.error(self.request, f"Le produit {produit.nom} n'est pas en stock.")
#                 return self.form_invalid(form)
#             total += produit.prix_unitaire * qte

#         # Création vente
#         vente = Vente.objects.create(boutique=boutique, utilisateur=utilisateur, date=timezone.now(), total=total)

#         # Création détails et mise à jour stock
#         for produit, qte in zip(produits, quantites):
#             stock = Stock.objects.get(boutique=boutique, produit=produit)
#             DetailVente.objects.create(vente=vente, produit=produit, quantite=qte, prix_unitaire=produit.prix_unitaire)
#             stock.quantite -= qte
#             stock.save()

#         messages.success(self.request, f"Vente N°{vente.id} enregistrée avec succès.")
#         return super().form_valid(form)

# def recu_pdf(request, vente_id):
#     vente = Vente.objects.get(id=vente_id)

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 800, f"Reçu vente N°{vente.id}")
#     p.drawString(100, 780, f"Boutique: {vente.boutique.nom}")
#     p.drawString(100, 760, f"Date: {vente.date.strftime('%d/%m/%Y %H:%M')}")

#     y = 740
#     for detail in vente.details.all():
#         text = f"{detail.produit.nom} - Qté: {detail.quantite} - Prix: {detail.prix_unitaire} €"
#         p.drawString(100, y, text)
#         y -= 20

#     p.drawString(100, y - 20, f"Total: {vente.total} €")
#     p.showPage()
#     p.save()
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='application/pdf')