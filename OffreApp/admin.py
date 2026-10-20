
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Offre


# ACTION 1 : Exporter les offres sélectionnées en CSV

@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="offres.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'reference_expedition',
        'transporteur',
        'prix',
        'statut'
    ])

    for offre in queryset.select_related('expedition', 'transporteur'):
        writer.writerow([
            offre.expedition.reference,
            offre.transporteur.raison_sociale,
            offre.prix,
            offre.statut
        ])

    return response


# ACTION 2 : Refuser plusieurs offres sélectionnées

@admin.action(description="Mettre les offres sélectionnées au statut Refusée")
def refuser_offres(modeladmin, request, queryset):

    nombre = queryset.update(statut='refusee')

    modeladmin.message_user(
        request,
        f"{nombre} offre(s) refusée(s) avec succès."
    )


# ADMINISTRATION DES OFFRES

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'expedition',
        'transporteur',
        'vehicule',
        'prix',
        'delai_jours',
        'statut_colore',
        'date_proposition'
    )

    list_filter = ('statut', 'date_proposition')

    search_fields = (
        'expedition__reference',
        'transporteur__raison_sociale',
        'vehicule__immatriculation'
    )

    list_editable = ('delai_jours',)

    ordering = ('-created_at',)

    date_hierarchy = 'date_proposition'

    list_per_page = 25

    autocomplete_fields = (
        'expedition',
        'transporteur',
        'vehicule'
    )

    readonly_fields = (
        'statut_colore',
        'date_proposition',
        'created_at',
        'updated_at'
    )

    fieldsets = (
        ('Détails de l’offre', {
            'fields': (
                'expedition',
                'transporteur',
                'vehicule'
            )
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours')
        }),
        ('Suivi', {
            'fields': (
                'statut',
                'statut_colore',
                'date_proposition',
                'created_at',
                'updated_at'
            )
        }),
    )

    # Actions disponibles
    actions = [exporter_offres_csv, refuser_offres]

    # Affichage coloré du statut
    @admin.display(description='Statut')
    def statut_colore(self, obj):

        if not obj or not obj.pk:
            return '-'

        couleurs = {
            'proposee': '#F0AD4E',
            'acceptee': '#5CB85C',
            'refusee': '#D9534F',
            'retiree': '#777777'
        }

        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#999999'),
            obj.get_statut_display()
        )

    # Protection des offres acceptées
    def get_readonly_fields(self, request, obj=None):

        base = list(self.readonly_fields)

        if obj and obj.statut == 'acceptee':
            return base + ['prix', 'delai_jours']

        return base
