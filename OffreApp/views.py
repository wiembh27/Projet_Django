
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Offre


def liste_offres(request):
    offres = (
        Offre.objects
        .select_related(
            'expedition',
            'transporteur',
            'vehicule'
        )
        .order_by('-date_proposition')
    )

    return render(
        request,
        'offre/liste.html',
        {'offres': offres}
    )


def detail_offre(request, pk):
    offre = get_object_or_404(
        Offre.objects.select_related(
            'expedition',
            'transporteur',
            'vehicule'
        ),
        pk=pk
    )

    return render(
        request,
        'offre/detail.html',
        {'offre': offre}
    )


@require_POST
def supprimer_offre(request, pk):
    offre = get_object_or_404(Offre, pk=pk)

    offre.delete()

    messages.success(
        request,
        "L'offre a été supprimée avec succès."
    )

    return redirect('offres:liste')
