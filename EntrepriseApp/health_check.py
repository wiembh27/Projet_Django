
from datetime import timedelta

from django.contrib import admin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from OffreApp.models import Offre


def health_check_view(request):

    # 1. Offres et expeditions incoherentes
    offres_incoherentes = Offre.objects.filter(
        Q(statut='acceptee') & ~Q(expedition__statut='attribuee')
        |
        Q(statut='proposee') & ~Q(expedition__statut='publiee')
    )

    # 2. Expeditions bloquees depuis plus de 7 jours
    limite = timezone.now() - timedelta(days=7)

    expeditions_bloquees = Expedition.objects.filter(
        statut='publiee',
        created_at__lt=limite
    )

    # 3. Transporteurs sans flotte
    transporteurs_sans_flotte = Entreprise.objects.filter(
        type_entreprise='transporteur'
    ).annotate(
        nb_vehicules=Count('Vehicule')
    ).filter(nb_vehicules=0)

    # 4. Doublons de propositions
    doublons = Offre.objects.filter(
        statut='proposee'
    ).values(
        'expedition__reference',
        'transporteur__raison_sociale'
    ).annotate(
        total=Count('id')
    ).filter(total__gt=1)

    context = {
        **admin.site.each_context(request),
        'title': "Controle d'integrite TransConnect",
        'offres_incoherentes': offres_incoherentes,
        'expeditions_bloquees': expeditions_bloquees,
        'transporteurs_sans_flotte': transporteurs_sans_flotte,
        'doublons': doublons,
    }

    return render(request, 'admin/health_check.html', context)


# Ajout d'une URL personnalisee dans Django Admin
ancien_get_urls = admin.site.get_urls


def get_urls():
    urls = ancien_get_urls()

    urls_personnalisees = [
        path(
            'health-check/',
            admin.site.admin_view(health_check_view),
            name='health_check'
        ),
    ]

    return urls_personnalisees + urls


admin.site.get_urls = get_urls
