import json
from decimal import Decimal
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db import transaction
from django.contrib import messages

from ..models import Vente
from ..forms.forms_vente import ClientForm

# class VenteCreateView(FormView):
#     template_name = "ventes/vente_dashboard.html"
#     form_class = ClientForm
#     success_url = "/ventes/"

#     @transaction.atomic
#     def form_valid(self, form):
#         items_json = self.request.POST.get("items")
#         if not items_json:
#             form.add_error(None, "⚠️ Aucun produit sélectionné.")
#             return self.form_invalid(form)

#         items = json.loads(items_json)

#         # --- 1. Client ---
#         client = form.save(commit=False)
#         client.boutique = self.request.user.boutique
#         client.save()

#         # --- 2. Total ---
#         total = sum(Decimal(str(i["price"])) * int(i["quantity"]) for i in items)

#         # --- 3. Vente ---
#         vente = Vente.objects.create(
#             client=client,
#             boutique=self.request.user.boutique,
#             utilisateur=self.request.user,
#             total=total,
#         )

#         # --- 4. Détails + MAJ Stock ---
#         for i in items:
#             produit = Produit.objects.get(pk=i["id"])
#             quantite = int(i["quantity"])
#             prix_unitaire = Decimal(str(i["price"]))

#             # Vérif stock
#             stock = StockCourant.objects.select_for_update().get(
#                 produit=produit, boutique=self.request.user.boutique
#             )
#             if stock.quantite < quantite:
#                 form.add_error(None, f"❌ Stock insuffisant pour {produit.nom}")
#                 transaction.set_rollback(True)
#                 return self.form_invalid(form)

#             # Création du détail
#             DetailVente.objects.create(
#                 vente=vente,
#                 produit=produit,
#                 quantite=quantite,
#                 prix_unitaire=prix_unitaire,
#             )

#             # Mise à jour stock
#             stock.quantite -= quantite
#             stock.save()

#         messages.success(self.request, "✅ Vente enregistrée avec succès")
#         # On redirige vers PDF (voir CBV ci-dessous)
#         return redirect("vente_pdf", pk=vente.pk)

class VentePDFView(DetailView):
    """Vue qui génère le PDF d'une vente"""

    model = Vente
    template_name = "PDF/vente_pdf.html"  # rendu HTML pour test si besoin

    def render_to_pdf(self, context):
        # Rendre le HTML en string
        html_string = render_to_string(self.template_name, context)
        # Convertir en PDF
        pdf_file = HTML(string=html_string).write_pdf()
        return pdf_file

    def get(self, request, *args, **kwargs):
        vente = self.get_object()
        context = {"vente": vente}

        pdf_file = self.render_to_pdf(context)
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="vente_{vente.pk}.pdf"'
        return response