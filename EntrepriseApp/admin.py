from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Entreprise
from VehiculeApp.models import Vehicule

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('user_id', 'username', 'email')
    ordering = ('username',)
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations TransConnect', {
            'fields': ('role', 'telephone', 'user_id', 'created_at', 'updated_at')
        }),
    )

class VehiculeInline(admin.TabularInline):
    model = Vehicule
    extra = 1 
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponibilite')
    extra = 1 
    show_change_link= True

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur', 'created_at')
    list_filter = ('type_entreprise','created_at')
    search_fields = ('raison_sociale', 'matricule_fiscal')
    ordering = ('raison_sociale',)
    autocomplete_fields = ('utilisateur',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

    fieldsets = (
        ('Informations de l’entreprise', {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'adresse')
        }),
        ('Gestion', {
            'fields': ('utilisateur',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
admin.site.site_header='Transconnect_Administration'
admin.site.site_title='TransConnect' #titre de l'onglet du navigateur
admin.site.index_title="Tableau de bord"