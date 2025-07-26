from django.http import JsonResponse
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
    template_name = 'stocks/stock_form.html'
    success_url = reverse_lazy('stock_list')
    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'form_html': html})
        return super().form_invalid(form)
class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock_form.html'
    success_url = reverse_lazy('stock_list')
class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock_confirm_delete.html'
    success_url = reverse_lazy('stock_list')