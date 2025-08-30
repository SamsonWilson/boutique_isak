from django.views import View
from django.shortcuts import render, redirect
from  ..forms.forms_vente import ClientForm, VenteForm, DetailVenteFormSet
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from ..models import 
from ..forms.forms_stock import StockForm,DateRangeForm, StockUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
# votre_app/views.py
from django.contrib import messages
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