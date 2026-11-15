
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Vehicule
from OffreApp.models import Offre


def liste_vehicules(request):
    vehicules = (
        Vehicule.objects
        .select_related('entreprise')
        .order_by('-created_at')
    )

    return render(
        request,
        'vehicule/liste.html',
        {'vehicules': vehicules}
    )


def detail_vehicule(request, pk):
    vehicule = get_object_or_404(
        Vehicule.objects.select_related('entreprise'),
        pk=pk
    )

    return render(
        request,
        'vehicule/detail.html',
        {'vehicule': vehicule}
    )


@require_POST
def supprimer_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)

    if Offre.objects.filter(vehicule=vehicule).exists():
        messages.error(
            request,
            "Impossible de supprimer ce véhicule : "
            "des offres lui sont associées."
        )
        return redirect('vehicules:detail', pk=pk)

    vehicule.delete()

    messages.success(
        request,
        "Le véhicule a été supprimé avec succès."
    )

    return redirect('vehicules:liste')
