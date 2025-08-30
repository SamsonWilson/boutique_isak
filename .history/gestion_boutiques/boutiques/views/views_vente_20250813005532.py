from django.shortcuts import render, redirect
from django.views import View
from ..models import Vente, DetailVente
from ..forms.forms_vente import VenteForm, DetailVenteFormSet

class VenteCreateView(View):
    template_name = 'ventes/vente_dashboard.html'

    def get(self, request):
        vente_form = VenteForm()
        detail_formset = DetailVenteFormSet()
        ventes = Vente.objects.prefetch_related('details', 'details__produit')
        return render(request, self.template_name, {
            'vente_form': vente_form,
            'detail_formset': detail_formset,
            'ventes': ventes,
        })
    
    def post(self, request):
        vente_form = VenteForm(request.POST)
        detail_formset = DetailVenteFormSet(request.POST)

        if vente_form.is_valid() and detail_formset.is_valid():
            vente = vente_form.save()
            details = detail_formset.save(commit=False)
            total = 0
            for detail in details:
                detail.vente = vente
                detail.save()
                total += detail.prix_unitaire * detail.quantite
            vente.total = total
            vente.save()
            return redirect('vente_dashboard')  # adapte à ton url name
        
        ventes = Vente.objects.prefetch_related('details', 'details__produit')
        return render(request, self.template_name, {
            'vente_form': vente_form,
            'detail_formset': detail_formset,
            'ventes': ventes,
        })
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