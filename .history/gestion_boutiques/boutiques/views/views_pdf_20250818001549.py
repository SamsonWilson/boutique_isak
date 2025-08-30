from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from weasyprint import HTML
from ..models import Vente

class VentePDFView(DetailView):
    """Vue qui génère le PDF d'une vente"""
    model = Vente
    template_name = "PDF/PDF_vente.html"  # Ton template HTML

    def render_to_pdf(self, context):
        # Rendre le template HTML en string
        html_string = render_to_string(self.template_name, context)

        # Convertir en PDF avec WeasyPrint
        pdf_file = HTML(string=html_string, base_url=self.request.build_absolute_uri()).write_pdf()

        return pdf_file

    def get(self, request, *args, **kwargs):
        vente = self.get_object()
        context = {"vente": vente}
        pdf_file = self.render_to_pdf(context)

        if not pdf_file:
            return HttpResponse("Erreur lors de la génération du PDF", status=500)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="vente_{vente.pk}.pdf"'
        return response