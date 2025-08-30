# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        current_view = request.resolver_match.view_name if request.resolver_match else None

        # --- 1. Pages publiques accessibles sans auth
        public_views = ["connexion", "logout"]
        if current_view in public_views:
            return None

        # --- 2. Vérification login
        if not request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "Non authentifié"}, status=401)
            return redirect(reverse("connexion"))

        # --- 3. Permissions par rôle
        role_permissions = {
            "admin": ["*", "vente_pdf"],   # admin a tous les droits
            "responsable": ["accueil", "produit_list", "vente_dashboard", "search_product"],
            "caissier": ["accueil", "vente_dashboard", "search_product",""],
        }

        role = getattr(request.user, "role", None)

        # --- 3.a Admin = accès total
        if role == "admin":
            return None

        allowed_views = role_permissions.get(role, [])

        # --- 3.b full accès via "*"
        if "*" in allowed_views:
            return None

        # --- 3.c vue autorisée
        if current_view in allowed_views:
            return None

        # --- 3.d accès refusé → JSON si AJAX, sinon rediriger
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": "Accès interdit"}, status=403)
        return redirect("accueil")









# # accounts/middleware.py
# from django.shortcuts import redirect
# from django.urls import reverse

# class RoleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         return self.get_response(request)

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Récupérer le nom de la vue
#         current_view = request.resolver_match.view_name if request.resolver_match else None

#         # ✅ Pages publiques non contrôlées (login & logout uniquement)
#         public_views = ["connexion", "logout"]

#         if current_view in public_views:
#             return None  # on laisse passer sans contrôle

#         # ✅ Si pas connecté → redirection login directement
#         if not request.user.is_authenticated:
#             return redirect(reverse("connexion"))

#         # ✅ Gestion des rôles
#         role_permissions = {
#             "admin": [
#                 # admin peut tout faire, on retourne None
#                 "*","vente_pdf"
#             ],
#             "responsable": [
#                 "accueil",
#                 "produit_list",
#                 "vente_dashboard",
#             ],
#             "caissier": [
#                 "accueil",
#                 "vente_dashboard",
                
#             ],
#         }

#         role = getattr(request.user, "role", None)

#         if role == "admin":
#             return None  # l’admin a accès à toutes les vues

#         allowed_views = role_permissions.get(role, [])

#         # si "*" dans allowed_views → full accès
#         if "*" in allowed_views:
#             return None

#         # si la vue est permise → on laisse passer
#         if current_view in allowed_views:
#             return None

#         # sinon redirection → login
#         return redirect(reverse("connexion"))
    


    