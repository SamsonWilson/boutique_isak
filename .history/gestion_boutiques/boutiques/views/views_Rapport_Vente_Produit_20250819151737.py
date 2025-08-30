# views.py
from django.views import View
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import now, timedelta
from ..models import Vente, DetailVente, StockCourant, Produit

class Dashboard_vente_produitView(View):
    template_name = "rapports/dashboard.html"

    def get(self, request):
        # 1. Totaux du jour
        today = now().date()
        ventes_jour = Vente.objects.filter(date__date=today)
        total_jour = ventes_jour.aggregate(total=Sum("total"))["total"] or 0

        # 2. 5 dernières ventes
        dernieres_ventes = Vente.objects.select_related("client", "utilisateur").order_by("-date")[:5]

        # 3. Les 5 produits les plus vendus (ce mois)
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

        # 4. Stocks courants (produits avec quantite faible)
        stocks_faibles = StockCourant.objects.filter(quantite__lte=5)

        context = {
            "total_jour": total_jour,
            "dernieres_ventes": dernieres_ventes,
            "top_produits": top_produits,
            "stocks_faibles": stocks_faibles,
        }
        return render(request, self.template_name, context)