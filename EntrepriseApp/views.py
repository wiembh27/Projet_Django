
from django.shortcuts import render, get_object_or_404
from .models import Entreprise


from django.http import HttpResponse

def home(request):
    return render(request, 'entreprise/home.html')


def liste_entreprises(request):
    entreprises = (
        Entreprise.objects
        .select_related('utilisateur')
        .order_by('raison_sociale')
    )

    return render(
        request,
        'entreprise/liste.html',
        {'entreprises': entreprises}
    )


def detail_entreprise(request, pk):
    entreprise = get_object_or_404(
        Entreprise.objects.select_related('utilisateur'),
        pk=pk
    )

    return render(
        request,
        'entreprise/detail.html',
        {'entreprise': entreprise}
    )
