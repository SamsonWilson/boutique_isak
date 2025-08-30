from django.contrib import admin
from .models import Boutique, Utilisateur
from django.contrib.auth.admin import UserAdmin

admin.site.register(Boutique)
admin.site.register(Utilisateur, UserAdmin)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)