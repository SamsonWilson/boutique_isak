# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Récupérer le nom de la vue
        current_view = request.resolver_match.view_name if request.resolver_match else None

        # ✅ Pages publiques non contrôlées (login & logout uniquement)
        public_views = ["connexion", "logout"]

        if current_view in public_views:
            return None  # on laisse passer sans contrôle

        # ✅ Si pas connecté → redirection login directement
        if not request.user.is_authenticated:
            return redirect(reverse("connexion"))

        # ✅ Gestion des rôles
        role_permissions = {
            "admin": [
                # admin peut tout faire, on retourne None
                "*",
            ],
            "responsable": [
                "accueil",
                "produit_list",
                "vente_dashboard",
            ],
            "caissier": [
                "accueil",
                "vente_dashboard",
                
            ],
        }

        role = getattr(request.user, "role", None)

        if role == "admin":
            return None  # l’admin a accès à toutes les vues

        allowed_views = role_permissions.get(role, [])

        # si "*" dans allowed_views → full accès
        if "*" in allowed_views:
            return None

        # si la vue est permise → on laisse passer
        if current_view in allowed_views:
            return None

        # sinon redirection → login
        return redirect(reverse("connexion"))