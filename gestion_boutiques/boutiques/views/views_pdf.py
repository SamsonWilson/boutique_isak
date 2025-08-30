from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from weasyprint import HTML
from ..models import Vente
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
import tempfile
from ..models import Inventaire
from io import BytesIO



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
    



class InventairePDFView(View):
    def get(self, request, pk):
        inventaire = Inventaire.objects.get(pk=pk)
        details = inventaire.details.all()

        template = get_template("PDF/inventaire_pdf.html")
        html_content = template.render({"inventaire": inventaire, "details": details})

        # Génère le PDF directement en mémoire
        pdf_file = BytesIO()
        HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(pdf_file)
        pdf_file.seek(0)

        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="inventaire_{inventaire.id}.pdf"'
        return response
