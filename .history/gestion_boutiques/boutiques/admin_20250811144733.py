from django.contrib import admin
from .models import Boutique, Utilisateur,CustomUser
from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser


admin.site.register(Boutique)
admin.site.register(Utilisateur, UserAdmin)
