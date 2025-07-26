from django.urls import path

from gestion_boutiques.boutiques.views.views_utilisateurs import ConnexionView

from .views.views_base import AccueilView

from .views.views_vente import VenteCreateView, recu_pdf
from .views.views_Boutique import BoutiqueListCreateView, BoutiqueRetrieveUpdateDestroyView

urlpatterns = [
    path('boutiques/', BoutiqueListCreateView.as_view(), name='boutique-list-create'),
    path('boutiques/<int:pk>/', BoutiqueRetrieveUpdateDestroyView.as_view(), name='boutique-detail'),
    path('v', VenteCreateView.as_view(), name='vente_creer'),
    path('vente/<int:vente_id>/recu/', recu_pdf, name='vente_recu'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),

    path('', AccueilView.as_view(), name='accueil'),
]