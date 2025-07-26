from django.contrib import admin

# Register your models here.
# dans le fichier admin.py de votre application

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Boutique, Utilisateur

# Personnalisation de l'affichage pour le modèle Utilisateur
class UtilisateurAdmin(UserAdmin):
    # Les champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'boutique')
    
    # Les filtres qui apparaîtront sur le côté droit
    list_filter = ('role', 'boutique', 'is_staff', 'is_superuser', 'groups')

    # Pour que les champs 'role' et 'boutique' apparaissent dans le formulaire de création/modification
    # On ajoute une nouvelle section au formulaire
    # On part des fieldsets de base de UserAdmin et on ajoute les nôtres
    fieldsets = UserAdmin.fieldsets + (
        ('Informations complémentaires', {'fields': ('role', 'boutique')}),
    )
    # C'est nécessaire aussi pour le formulaire d'ajout d'utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations complémentaires', {'fields': ('role', 'boutique')}),
    )

# Enregistrement du modèle Boutique pour qu'il soit gérable dans l'admin
admin.site.register(Boutique)

# Enregistrement du modèle Utilisateur avec sa configuration personnalisée
admin.site.register(Utilisateur, UtilisateurAdmin)