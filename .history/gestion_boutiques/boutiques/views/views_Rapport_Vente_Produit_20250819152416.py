# views.py
from django.views import View
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import now, timedelta
from ..models import Vente, DetailVente, StockCourant, Produit
import json
class DashboardView(View):
    template_name = "rapports/dashboard.html"

    def get(self, request):
        today = now().date()
        ventes_jour = Vente.objects.filter(date__date=today)
        total_jour = ventes_jour.aggregate(total=Sum("total"))["total"] or 0

        dernieres_ventes = Vente.objects.select_related("client", "utilisateur").order_by("-date")[:5]

        debut_mois = today.replace(day=1)
        details_mois = DetailVente.objects.filter(vente__date__date__gte=debut_mois)

        top_produits = (
            details_mois.values("produit__nom")
            .annotate(
                quantite_totale=Sum("quantite"),
                chiffre_affaire=Sum(F("quantite") * F("prix_unitaire")),
            )
            .order_by("-quantite_totale")[:5]
        )

        stocks_faibles = StockCourant.objects.filter(quantite__lte=5)

        # EXTRACTION pour éviter le pluck côté template
        labels = [p["produit__nom"] for p in top_produits]
        quantites = [p["quantite_totale"] or 0 for p in top_produits]
        ca = [float(p["chiffre_affaire"] or 0) for p in top_produits]

        context = {
            "total_jour": total_jour,
            "dernieres_ventes": dernieres_ventes,
            "stocks_faibles": stocks_faibles,
            # JSON pour Chart.js
            "labels_json": json.dumps(labels),
            "quantites_json": json.dumps(quantites),
            "ca_json": json.dumps(ca),
        }
        return render(request, self.template_name, context)