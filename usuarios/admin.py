# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'status')
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Customizados', {'fields': ('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Customizados', {'fields': ('role', 'status')}),
    )

    # --- CLASSE ADICIONADA PARA CARREGAR O JAVASCRIPT ---
    class Media:
        # O caminho é relativo à pasta 'static'
        js = ('js/show_password.js',)
    # ----------------------------------------------------

admin.site.register(User, CustomUserAdmin)
