from django.contrib import admin
from .models import Boutique, Utilisateur
from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

admin.site.register(Boutique)
admin.site.register(Utilisateur, UserAdmin)


class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role',)
        }),
    )
admin.site.register(Utilisateur, UserAdmin)

# admin.site.register(Utilisateur, UtilisateurAdmin)
