from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Stock
from ..forms.forms_stock import StockForm
class StockListView(ListView):
    model = Stock
    template_name = 'stock_list.html'
    context_object_name = 'stocks'

class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'sockets/stock_form.html'
    success_url = reverse_lazy('stock_list')
class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')
class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock_confirm_delete.html'
    success_url = reverse_lazy('stock_list')