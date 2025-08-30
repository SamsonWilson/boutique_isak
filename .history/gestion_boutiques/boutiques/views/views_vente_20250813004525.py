from django.views import View
from django.shortcuts import render, redirect
from  ..forms.forms import ClientForm, VenteForm, DetailVenteFormSet

class VenteCreateView(View):
    template_name = "enregistrement_vente.html"

    def get(self, request):
        client_form = ClientForm()
        vente_form = VenteForm()
        formset = DetailVenteFormSet()
        return render(request, self.template_name, {
            'client_form': client_form,
            'vente_form': vente_form,
            'formset': formset
        })

    def post(self, request):
        client_form = ClientForm(request.POST)
        vente_form = VenteForm(request.POST)
        formset = DetailVenteFormSet(request.POST)
        if client_form.is_valid() and vente_form.is_valid():
            client = client_form.save()
            vente = vente_form.save(commit=False)
            vente.client = client  # Associe le client à la vente
            vente.save()
            formset = DetailVenteFormSet(request.POST, instance=vente)
            if formset.is_valid():
                formset.save()
                return redirect('success_page')  # À adapter
        # Si erreur, on affiche les formulaires avec les erreurs
        return render(request, self.template_name, {
            'client_form': client_form,
            'vente_form': vente_form,
            'formset': formset
        })