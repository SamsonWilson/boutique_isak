from django.shortcuts import render, redirect
from django.views import View
from ..models import Vente, DetailVente
from ..forms.forms_vente import ClientForm, VenteForm, DetailVenteFormSet
# dans votre ventes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class VenteCreateView(LoginRequiredMixin, View):
    template_name = 'ventes/vente_dashboard.html' # Le template que vous avez montré

    def get(self, request, *args, **kwargs):
        # Initialise les formulaires pour la requête GET
        vente_form = VenteForm()
        client_form = ClientForm()
        formset = DetailVenteFormSet()
        context = {
            'vente_form': vente_form,
            'client_form': client_form,
            'formset': formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Traite les données soumises
        vente_form = VenteForm(request.POST)
        client_form = ClientForm(request.POST)
        formset = DetailVenteFormSet(request.POST)

        # Vérifie si tous les formulaires sont valides
        if vente_form.is_valid() and client_form.is_valid() and formset.is_valid():
            
            # 1. Ne sauvegardez pas encore la vente en base de données
            # `commit=False` crée l'objet en mémoire sans l'envoyer à la BDD.
            vente = vente_form.save(commit=False)

            # 2. Assignez l'utilisateur et sa boutique à l'objet vente
            vente.utilisateur = request.user
            vente.boutique = request.user.boutique # Ceci suppose que votre modèle Utilisateur a un champ 'boutique'

            # 3. Maintenant, sauvegardez l'objet Vente principal
            # Il aura maintenant un ID, nécessaire pour les détails de la vente.
            vente.save()
            
            # Traitez le client (créez-le ou récupérez-le)
            client = client_form.save()
            vente.client = client # Liez le client à la vente
            vente.save(update_fields=['client']) # Mettez à jour juste ce champ

            # 4. Traitez le formset (détails de la vente)
            details = formset.save(commit=False)
            for detail in details:
                detail.vente = vente # Liez chaque détail à la vente que nous venons de créer
                detail.save()
                # --- !! IMPORTANT !! ---
                # C'est ici que vous devriez aussi mettre à jour votre stock !
                # Exemple : StockActuel.objects.filter(produit=detail.produit, boutique=vente.boutique).update(...)

            # N'oubliez pas de sauvegarder les relations ManyToMany si le formset en a
            formset.save_m2m()

            # Redirigez vers une page de succès
            return redirect('nom_de_votre_url_de_succes_vente')
        
        # Si les formulaires ne sont pas valides, ré-affichez la page avec les erreurs
        context = {
            'vente_form': vente_form,
            'client_form': client_form,
            'formset': formset,
        }
        return render(request, self.template_name, context)
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