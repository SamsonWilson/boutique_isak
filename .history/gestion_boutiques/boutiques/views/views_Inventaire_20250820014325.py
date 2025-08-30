from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Inventaire, InventaireDetail, Produit, Boutique,StockCourant

class InventaireCreateView(View):
    template_name = "inventaire/inventaire_creer.html"

    def get(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        # Liste des stocks courants de la boutique
        stocks = MouvementStock.objects.filter(boutique=boutique).select_related("produit")

        return render(request, self.template_name, {
            "boutique": boutique,
            "stocks": stocks
        })

    def post(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        # 1️⃣ Créer l’inventaire
        inventaire = Inventaire.objects.create(
            utilisateur=request.user,
            boutique=boutique,
            description=request.POST.get("description", "")
        )

        # 2️⃣ Créer les détails en parcourant StockCourant
        stocks = StockCourant.objects.filter(boutique=boutique).select_related("produit")
        for stock in stocks:
            produit = stock.produit
            stock_theorique = stock.quantite
            stock_reel = int(request.POST.get(f"stock_reel_{produit.id}", 0))

            # Ligne de détail d’inventaire
            InventaireDetail.objects.create(
                inventaire=inventaire,
                produit=produit,
                stock_theorique=stock_theorique,
                stock_reel=stock_reel
            )

            # 🔹 Mise à jour du stock courant
            stock.quantite = stock_reel
            stock.save(update_fields=["quantite"])

        return redirect("inventaire_detail", pk=inventaire.id)
    
from django.views.generic import DetailView

class InventaireDetailView(DetailView):
    model = Inventaire
    template_name = "inventaire/inventaire_detail.html"
    context_object_name = "inventaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details"] = self.object.details.all()
        return context    