from django.shortcuts import redirect
from django.urls import reverse

class RoleMiddleware:
    """
    Middleware qui contrôle l'accès aux URLS en fonction du rôle de l'utilisateur
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        if not request.user.is_authenticated:
            return None  # Laisse gérer le LoginRequiredMixin ou la vue Login

        # --- Mapping des accès ---
        role_permissions = {
            "admin": [
                "/utilisateurs/", "/produits/", "/stocks/", "/ventes/", "/boutiques/"
            ],
            "gerant": [
                "/produits/", "/stocks/", "/ventes/"
            ],
            "vendeur": [
                "/ventes/"
            ],
        }

        # Rôle de l’utilisateur en cours
        role = getattr(request.user, "role", None)
        if role not in role_permissions:
            return redirect(reverse("accueil"))

        # Vérifier si l'URL demandée correspond aux autorisations
        for path in role_permissions[role]:
            if request.path.startswith(path):
                return None  # autorisé

        # Si aucune correspondance → accès refusé
        return redirect(reverse("connexion"))