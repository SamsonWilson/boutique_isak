from django.urls import path
from .views.views_Boutique import BoutiqueListCreateView, BoutiqueRetrieveUpdateDestroyView

urlpatterns = [
    path('boutiques/', BoutiqueListCreateView.as_view(), name='boutique-list-create'),
    path('boutiques/<int:pk>/', BoutiqueRetrieveUpdateDestroyView.as_view(), name='boutique-detail'),
]