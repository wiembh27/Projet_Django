
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InscriptionForm, EntrepriseForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise
from .forms import InscriptionForm
from django.contrib.auth import login
from django.urls import reverse_lazy


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

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            return redirect('entreprises:ajouter')
    else:
        form = InscriptionForm()

    return render(request, 'registration/inscription.html', {'form': form})     
class InscriptionView(CreateView):
    form_class = InscriptionForm
    template_name = 'offre/inscription.html'
    success_url = reverse_lazy('entreprises:ajouter')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class EntrepriseCreateView(LoginRequiredMixin, CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprise/form.html'
    success_url = reverse_lazy('expedition:liste')

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        return super().form_valid(form)

class EntrepriseCreateView(LoginRequiredMixin, CreateView):
    model = Entreprise
    fields = ['raison_sociale', 'matricule_fiscal', 'type_entreprise', 'adresse']
    template_name = 'entreprise/form.html'
    success_url = reverse_lazy('expedition:liste')

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        return super().form_valid(form)