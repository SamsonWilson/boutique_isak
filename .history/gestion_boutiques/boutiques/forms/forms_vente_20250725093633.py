from django import forms
from .models import Produit

class VenteForm(forms.Form):
    produits = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    quantites = forms.CharField(help_text="Quantités séparées par des virgules, dans le même ordre que les produits sélectionnés")

    def clean(self):
        cleaned_data = super().clean()
        produits = cleaned_data.get('produits')
        quantites = cleaned_data.get('quantites')

        if produits and quantites:
            quantites_list = quantites.split(',')
            if len(quantites_list) != produits.count():
                raise forms.ValidationError("Le nombre de quantités doit correspondre au nombre de produits sélectionnés.")

            try:
                quantites_int = [int(q.strip()) for q in quantites_list]
                if any(q <= 0 for q in quantites_int):
                    raise forms.ValidationError("Toutes les quantités doivent être des entiers positifs.")
            except ValueError:
                raise forms.ValidationError("Les quantités doivent être des nombres entiers.")

            cleaned_data['quantites_list'] = quantites_int

        return cleaned_data