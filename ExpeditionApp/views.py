
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Expedition
from OffreApp.models import Offre


def home(request):
    return HttpResponse("<h1>Welcome to Expeditions</h1>")


def welcome(request, name):
    return HttpResponse(f"Hello {name}")


def listExpeditions(request):
    expeditions = (
        Expedition.objects
        .filter(statut='publiee')
        .select_related('entreprise')
        .order_by('-created_at')
    )

    return render(
        request,
        'expedition/list.html',
        {'expeditions': expeditions, 'liste': expeditions}
    )


def detailsExpedition(request, pk):
    expedition = get_object_or_404(
        Expedition.objects.select_related('entreprise'),
        pk=pk
    )

    offres = (
        Offre.objects
        .filter(expedition=expedition)
        .select_related('transporteur', 'vehicule')
        .order_by('-date_proposition')
    )

    return render(
        request,
        'expedition/details.html',
        {
            'expedition': expedition,
            'exp': expedition,
            'offres': offres
        }
    )


def detail_expedition_reference(request, reference):
    expedition = get_object_or_404(
        Expedition,
        reference=reference
    )

    return detailsExpedition(request, expedition.pk)


@require_POST
def deleteExpedition(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    expedition.delete()

    return redirect('expedition:liste')
