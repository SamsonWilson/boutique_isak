from django import forms
from .models import Client, Vente, DetailVente

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})  # Ajoute la classe Bootstrap

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VenteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class DetailVenteForm(forms.ModelForm):
    class Meta:
        model = DetailVente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DetailVenteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})