from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Inventaire, InventaireDetail, MouvementStock, Produit, Boutique,StockCourant
from django.db.models import Sum, Q
from datetime import datetime

class InventaireCreateView(View):
    template_name = "inventaire/inventaire_creer.html"

    def get(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        # 🔹 Récupération des dates envoyées par GET (ou par défaut tout l’historique)
        date_debut = request.GET.get("date_debut")
        date_fin = request.GET.get("date_fin")

        mouvements = MouvementStock.objects.filter(boutique=boutique)

        if date_debut and date_fin:
            try:
                debut = datetime.strptime(date_debut, "%Y-%m-%d")
                fin = datetime.strptime(date_fin, "%Y-%m-%d")
                mouvements = mouvements.filter(date_mouvement__range=(debut, fin))
            except:
                pass

        # 🔹 Calcul du stock théorique par produit
        produits_data = []
        for produit in MouvementStockProduit.objects.all():
            entrees = mouvements.filter(produit=produit, type_mouvement="entrée").aggregate(total=Sum("quantite"))["total"] or 0
            sorties = mouvements.filter(produit=produit, type_mouvement="sortie").aggregate(total=Sum("quantite"))["total"] or 0
            stock_theorique = entrees - sorties

            produits_data.append({
                "produit": produit,
                "stock_theorique": stock_theorique
            })

        return render(request, self.template_name, {
            "boutique": boutique,
            "produits_data": produits_data,
            "date_debut": date_debut,
            "date_fin": date_fin,
        })

    def post(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        # 1️⃣ Créer l’inventaire
        inventaire = Inventaire.objects.create(
            utilisateur=request.user,
            boutique=boutique,
            description=request.POST.get("description", "")
        )

        # 2️⃣ Parcourir les produits
        for produit in Produit.objects.all():
            stock_theorique = int(request.POST.get(f"stock_theorique_{produit.id}", 0))
            stock_reel = int(request.POST.get(f"stock_reel_{produit.id}", 0))
            ecart = stock_reel - stock_theorique

            # Détail inventaire
            InventaireDetail.objects.create(
                inventaire=inventaire,
                produit=produit,
                stock_theorique=stock_theorique,
                stock_reel=stock_reel
            )

            # Si écart → mouvement correctif
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
    # template_name = "inventaire/inventaire_creer.html"

    # def get(self, request, boutique_id):
    #     boutique = get_object_or_404(Boutique, pk=boutique_id)

    #     # Liste des stocks courants de la boutique
    #     stocks = MouvementStock.objects.filter(boutique=boutique).select_related("produit")

    #     return render(request, self.template_name, {
    #         "boutique": boutique,
    #         "stocks": stocks
    #     })

    # def post(self, request, boutique_id):
    #     boutique = get_object_or_404(Boutique, pk=boutique_id)

    #     # 1️⃣ Créer l’inventaire
    #     inventaire = Inventaire.objects.create(
    #         utilisateur=request.user,
    #         boutique=boutique,
    #         description=request.POST.get("description", "")
    #     )

    #     # 2️⃣ Créer les détails en parcourant StockCourant
    #     stocks = StockCourant.objects.filter(boutique=boutique).select_related("produit")
    #     for stock in stocks:
    #         produit = stock.produit
    #         stock_theorique = stock.quantite
    #         stock_reel = int(request.POST.get(f"stock_reel_{produit.id}", 0))

    #         # Ligne de détail d’inventaire
    #         InventaireDetail.objects.create(
    #             inventaire=inventaire,
    #             produit=produit,
    #             stock_theorique=stock_theorique,
    #             stock_reel=stock_reel
    #         )

    #         # 🔹 Mise à jour du stock courant
    #         stock.quantite = stock_reel
    #         stock.save(update_fields=["quantite"])

    #     return redirect("inventaire_detail", pk=inventaire.id)
    
from django.views.generic import DetailView

class InventaireDetailView(DetailView):
    model = Inventaire
    template_name = "inventaire/inventaire_detail.html"
    context_object_name = "inventaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details"] = self.object.details.all()
        return context    