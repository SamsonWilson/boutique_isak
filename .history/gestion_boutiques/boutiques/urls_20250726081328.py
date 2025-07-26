from django.urls import path

from .views.views_produit import ProduitListView,ProduitDetailView,ProduitCreateView,ProduitUpdateView,ProduitDeleteView
from .views.views_utilisateurs import ConnexionView
from .views.views_base import AccueilView
from .views.views_vente import VenteCreateView, recu_pdf
from .views.views_Boutique import BoutiqueListCreateView, BoutiqueRetrieveUpdateDestroyView
namespace = 'Produits'
urlpatterns = [
    path('boutiques/', BoutiqueListCreateView.as_view(), name='boutique-list-create'),
    path('boutiques/<int:pk>/', BoutiqueRetrieveUpdateDestroyView.as_view(), name='boutique-detail'),
    path('v', VenteCreateView.as_view(), name='vente_creer'),
    path('vente/<int:vente_id>/recu/', recu_pdf, name='vente_recu'),
    path('', ConnexionView.as_view(), name='connexion'),
    # path('deconnexion/', LogoutView.as_view(), name='deconnexion'),
    path('accueil/', AccueilView.as_view(), name='accueil'),
    # produit 
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/<int:pk>/', ProduitDetailView.as_view(), name='produit_detail'),
    path('produits/ajouter/', ProduitCreateView.as_view(), name='produit_create'),
    path('produits/<int:pk>/modifier/', ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/<int:pk>/supprimer/', ProduitDeleteView.as_view(), name='produit_delete'),


    
]