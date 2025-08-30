from django import views
from django.urls import path

from .views.views_Rapport_Vente_Produit import Dashboard_vente_produitView

from .views.views_pdf import InventairePDFView, VentePDFView

from .views.views_Inventaire import InventaireCreateView, InventaireDetailListeView, InventaireDetailView, InventaireListView

from .views.views_vente import ProductSearchView, VenteCreateView, VenteListView

from .views.views_stock import ProduitStockDetailView, RapportStockView, StockCourantListView, StockDetailView, StockListView,StockCreateView,StockUpdateView,StockDeleteView
from .views.views_produit import DashboardView, ProduitDetailView,ProduitCreateView, ProduitListView,ProduitUpdateView,ProduitDeleteView
from .views.views_utilisateurs import AdminUserCreateView, ConnexionView, ToggleUserStatusView, UtilisateurListView, UtilisateurUpdateView
from .views.views_base import AccueilView
# from .views.views_vente import VenteCreateView, recu_pdf
from .views.views_Boutique import BoutiqueListCreateView, BoutiqueListView, BoutiqueRetrieveUpdateDestroyView
namespace = 'Produits'
namespace = 'stocks'
urlpatterns = [
    path('boutiques/', BoutiqueListCreateView.as_view(), name='boutique-list-create'),
    path('boutiques/<int:pk>/', BoutiqueRetrieveUpdateDestroyView.as_view(), name='boutique-detail'),
    path("boutique_liste/", BoutiqueListView.as_view(), name="boutique_liste"),

    # path('v', VenteCreateView.as_view(), name='vente_creer'),
    # path('vente/<int:vente_id>/recu/', recu_pdf, name='vente_recu'),
    path('', ConnexionView.as_view(), name='connexion'),
    # path('deconnexion/', LogoutView.as_view(), name='deconnexion'),
    path('accueil/', AccueilView.as_view(), name='accueil'),
    # produit 
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/<int:pk>/', ProduitDetailView.as_view(), name='produit_detail'),
    path('produits/ajouter/', ProduitCreateView.as_view(), name='produit_create'),
    path('produits/<int:pk>/modifier/', ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/<int:pk>/supprimer/', ProduitDeleteView.as_view(), name='produit_delete'),

# stock et vente
    path("dashboard_vente_produit/", Dashboard_vente_produitView.as_view(), name="dashboard_vente_produit"),
# stock
    path('stocks/', StockListView.as_view(), name='stock_list'),
    path('stocks/add/', StockCreateView.as_view(), name='stock_add'),
    path('stocks/<int:pk>/edit/', StockUpdateView.as_view(), name='stock_edit'),
    path('stocks/<int:pk>/delete/', StockDeleteView.as_view(), name='stock_delete'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name='stock_detail'),
    path("stocks_courant/", StockCourantListView.as_view(), name="liste_stocks"),
    path("stocks/produit/<int:produit_id>/", ProduitStockDetailView.as_view(), name="detail_produit_stock"),
    path("rapport-stock/", RapportStockView.as_view(), name="rapport_stock"),
    # path('<int:pk>/modifier/', StockUpdateView.as_view(), name='stock_update'),


    path('ventes/', VenteCreateView.as_view(), name="vente_dashboard"),
    path("search_product/", ProductSearchView.as_view(), name="search_product"),
    path("ventes_pdf/<int:pk>/pdf/", VentePDFView.as_view(), name="vente_pdf"),
    path("ventes_liste/", VenteListView.as_view(), name="liste_ventes"),
# Inventaire
    # path('inventaire/', InventaireListView.as_view(), name="inventaire_dashboard"),
    # path('inventaire/detail_vente/', Detail_venteListView.as_view(), name="detail_vente_dashboard"),
    path("inventaire/creer/<int:boutique_id>/", InventaireCreateView.as_view(), name="inventaire_creer"),
    path("inventaire/<int:pk>/", InventaireDetailView.as_view(), name="inventaire_detail"),
    path("inventaire/liste/<int:boutique_id>/", InventaireListView.as_view(), name="inventaire_list"),
    path("inventaire/detail/<int:pk>/", InventaireDetailListeView.as_view(), name="inventaire_detail_list"),
    path("inventaire/<int:pk>/pdf/", InventairePDFView.as_view(), name="inventaire_pdf"),


# Utilisateurs
    path('utilisateur/ajouter/', AdminUserCreateView.as_view(), name='add_utilisateur'),
    path("utilisateurs/", UtilisateurListView.as_view(), name="utilisateur_list"),
    path("utilisateurs/<int:pk>/modifier/", UtilisateurUpdateView.as_view(), name="utilisateur_edit"),    
    path('users/<int:pk>/toggle-status/', ToggleUserStatusView.as_view(), name='user_toggle_status'),
]