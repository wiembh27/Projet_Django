from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Expedition
from OffreApp.models import Offre


class EnRetardFilter(admin.SimpleListFilter):
    title = 'En retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return [('oui', 'Oui'), ('non', 'Non')]

    def queryset(self, request, queryset):
        aujourd_hui=timezone.now().date()
        if self.value() == 'oui':
            return queryset.filter(
                statut='publiee',
                date_souhaitee__lt=aujourd_hui
            )
        if self.value() == 'non':
            return queryset.exclude(
                statut='publiee',
                date_souhaitee__lt=aujourd_hui
            )
        return queryset


class OffreInline(admin.TabularInline):
    model = Offre
    extra = 0
    fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):

    list_display = (
        'reference',
        'entreprise',
        'ville_depart',
        'ville_arrivee',
        'statut_colore',
        'date_souhaitee'
    )

    list_filter = ('statut', 'ville_depart', EnRetardFilter)

    search_fields = ('reference', 'entreprise__raison_sociale')

    list_editable = ('date_souhaitee',)

    ordering = ('-created_at',)

    date_hierarchy = 'date_souhaitee'

    list_per_page = 25

    autocomplete_fields = ('entreprise',)

    readonly_fields = ('reference', 'created_at', 'updated_at', 'statut_colore') #attribut qu on peut voir sans les modifier

    inlines = [OffreInline]

    fieldsets = (
        ('Informations de l’expédition', {
            'fields': (
                'reference',
                'entreprise',
                'ville_depart',
                'ville_arrivee',
                'poids_kg',
                'date_souhaitee',
                'description'
            )
        }),
        ('Suivi', {
            'fields': ('statut', 'statut_colore')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        if not obj or not obj.pk:
            return '-'

        couleurs = {
            'publiee': '#F0AD4E',
            'attribuee': '#337AB7',
            'en_cours': '#5BC0DE',
            'livree': '#5CB85C',
            'annulee': '#D9534F'
        }

        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#777777'),
            obj.get_statut_display()
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        compteur = 0

        for expedition in queryset.filter(statut='en_cours'):
            expedition.statut = 'livree'
            expedition.full_clean()
            expedition.save()
            compteur += 1

        self.message_user(
            request,
            f"{compteur} expédition(s) clôturée(s) avec succès."
        )

    actions = ['cloturer_expeditions']


#admin.site.register(Vehicule,VehiculeAdmin)