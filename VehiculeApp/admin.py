from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):

    list_display = (
        'immatriculation',
        'type_vehicule',
        'capacite_kg',
        'disponibilite',
        'entreprise'
    )

    list_filter = ('type_vehicule', 'disponibilite')

    search_fields = (
        'immatriculation',
        'entreprise__raison_sociale'
    )

    list_editable = ('disponibilite',)

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')

    autocomplete_fields = ('entreprise',)

    list_per_page = 25

    fieldsets = (
        ('Informations du véhicule', {
            'fields': (
                'immatriculation',
                'type_vehicule',
                'capacite_kg'
            )
        }),
        ('Affectation et disponibilité', {
            'fields': ('entreprise', 'disponibilite')
        }),
        ('Historique', {
            'fields': ('created_at', 'updated_at')
        }),
    )
