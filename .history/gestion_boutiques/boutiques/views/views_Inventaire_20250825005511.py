from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import DetailVente, Inventaire, InventaireDetail, MouvementStock, Produit, Boutique,StockCourant
from django.db.models import Sum, Q
from datetime import datetime
from django.views.generic import DetailView
from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta

class InventaireCreateView(View):
    template_name = "inventaire/inventaire_creer.html"

    def get(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        date_debut_str = request.GET.get("date_debut")
        date_fin_str = request.GET.get("date_fin")

        mouvements = MouvementStock.objects.filter(boutique=boutique)
        ventes = DetailVente.objects.filter(vente__boutique=boutique)  # 🔹 seulement cette boutique

        if date_debut_str and date_fin_str:
            try:
                debut_naive = datetime.strptime(date_debut_str, "%Y-%m-%d")
                fin_naive = datetime.strptime(date_fin_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

                debut = timezone.make_aware(debut_naive, timezone.get_current_timezone())
                fin = timezone.make_aware(fin_naive, timezone.get_current_timezone())

                mouvements = mouvements.filter(date_mouvement__range=(debut, fin))
                ventes = ventes.filter(vente__date_vente__range=(debut, fin))
            except Exception as e:
                print("Erreur parsing date:", e)
                pass

        # 🔹 Produits uniquement affectés à la boutique
        produits = Produit.objects.filter(stockcourant__boutique=boutique).distinct()

        produits_data = []
        for produit in produits:
            entrees = mouvements.filter(produit=produit, type_mouvement="entrée").aggregate(total=Sum("quantite"))["total"] or 0
            sorties = mouvements.filter(produit=produit, type_mouvement="sortie").aggregate(total=Sum("quantite"))["total"] or 0
            vendu = ventes.filter(produit=produit).aggregate(total=Sum("quantite"))["total"] or 0

            stock_theorique = entrees - sorties - vendu

            produits_data.append({
                "produit": produit,
                "entrees": entrees,
                "sorties": sorties,
                "vendu": vendu,
                "stock_theorique": stock_theorique,
            })

        return render(request, self.template_name, {
            "boutique": boutique,
            "produits_data": produits_data,
            "date_debut": date_debut_str,
            "date_fin": date_fin_str,
        })

    def post(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        inventaire = Inventaire.objects.create(
            utilisateur=request.user,
            boutique=boutique,
            description=request.POST.get("description", "")
        )

        produits = Produit.objects.filter(stockcourant__boutique=boutique).distinct()

        for produit in produits:
            stock_theorique = int(request.POST.get(f"stock_theorique_{produit.id}", 0))
            stock_reel = int(request.POST.get(f"stock_reel_{produit.id}", 0))
            ecart = stock_reel - stock_theorique

            InventaireDetail.objects.create(
                inventaire=inventaire,
                produit=produit,
                stock_theorique=stock_theorique,
                stock_reel=stock_reel,
                stock_vendu=int(request.POST.get(f"stock_vendu_{produit.id}", 0))  # 🔹 si tu veux garder l’info
            )

            if ecart != 0:
                MouvementStock.objects.create(
                    boutique=boutique,
                    produit=produit,
                    quantite=abs(ecart),
                    type_mouvement="entrée" if ecart > 0 else "sortie",
                    description=f"Correction inventaire #{inventaire.id}",
                    utilisateur=request.user
                )

        return redirect("inventaire_detail", pk=inventaire.id)

    


class InventaireListView(ListView):
    model = Inventaire
    template_name = "inventaire/inventaire_list.html"
    context_object_name = "inventaires"

    def get_queryset(self):
        boutique_id = self.kwargs.get("boutique_id")
        self.boutique = get_object_or_404(Boutique, pk=boutique_id)
        return Inventaire.objects.filter(boutique=self.boutique).order_by("-date_creation")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["boutique"] = self.boutique
        return context
class InventaireDetailView(DetailView):
    model = Inventaire
    template_name = "inventaire/inventaire_detail.html"
    context_object_name = "inventaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # grâce à related_name="details", tu peux accéder direct ici
        context["details"] = self.object.details.all()
        return context


class InventaireDetailView(DetailView):
    model = Inventaire
    template_name = "inventaire/inventaire_detail.html"
    context_object_name = "inventaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details"] = self.object.details.all()
        return context    