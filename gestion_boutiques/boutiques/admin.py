from django.contrib import admin
from .models import Boutique, Utilisateur
from django.contrib.auth.admin import UserAdmin

admin.site.register(Boutique)
admin.site.register(Utilisateur, UserAdmin)