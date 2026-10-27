from django.shortcuts import render
from django.http import HttpResponse
from .models import Expedition
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return HttpResponse("<h1>Welcome to Expeditions</h1>")

def welcome(request, name):
    return HttpResponse(f"Hello {name}")

def listExpeditions(request):
    liste = Expedition.objects.all()
    return render(request, 'expedition/list.html', {"liste": liste})

def detailsExpedition(request, pk):
    expedition = Expedition.objects.get(pk=pk)
    return render(request, 'expedition/details.html', {'exp': expedition})

#DANS VIEWS TOUJOURS FAIRE UN RETURN POUR LES FONCTIONS

def deleteExpedition(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)

    if request.method == "POST":
        expedition.delete()
        return redirect('expedition:list')

    return redirect('expedition:details', pk=pk)