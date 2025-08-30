from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Inventaire, InventaireDetail, Produit, Boutique

class InventaireCreateView(View):
    template_name = "inventaire/inventaire_creer.html"

    def get(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)
        produits = stockcourant.objects.filter(boutique=boutique)  # selon ton modèle
        return render(request, self.template_name, {
            "boutique": boutique,
            "produits": produits
        })

    def post(self, request, boutique_id):
        boutique = get_object_or_404(Boutique, pk=boutique_id)

        # 1. Créer l’inventaire
        inventaire = Inventaire.objects.create(
            utilisateur=request.user,
            boutique=boutique,
            description=request.POST.get("description", "")
        )

        # 2. Créer les détails
        produits = Produit.objects.filter(boutique=boutique)
        for produit in produits:
            stock_theorique = produit.stock  # si ton modèle "Produit" contient un champ stock
            stock_reel = int(request.POST.get(f"stock_reel_{produit.id}", 0))

            InventaireDetail.objects.create(
                inventaire=inventaire,
                produit=produit,
                stock_theorique=stock_theorique,
                stock_reel=stock_reel
            )

        return redirect("inventaire_detail", pk=inventaire.id)
    
from django.views.generic import DetailView

class InventaireDetailView(DetailView):
    model = Inventaire
    template_name = "inventaire_detail.html"
    context_object_name = "inventaire"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details"] = self.object.details.all()
        return context    