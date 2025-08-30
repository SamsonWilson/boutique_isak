from django.shortcuts import redirect
from django.urls import reverse

class RoleMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None  

        current_view = request.resolver_match.view_name  # récupère le nom de la vue "app_name:view_name"

        # vues accessibles par tout le monde
        public_views = ["accueil", "login", "logout"]
        if current_view in public_views:
            return None

        role_permissions = {
            "admin":    ["utilisateur_list", "produit_list", "vente_dashboard", "boutique_liste"],
            "gerant":   ["produit_list", "vente_dashboard"],
            "vendeur":  ["vente_dashboard"],
        }

        allowed_views = role_permissions.get(getattr(request.user, "role", None), [])

        if current_view not in allowed_views:
            return redirect("accueil")

        return None