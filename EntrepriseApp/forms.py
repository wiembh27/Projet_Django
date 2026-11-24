from django import forms
from .models import Entreprise, Utilisateur
from django.contrib.auth.forms import UserCreationForm


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['raison_sociale', 'matricule_fiscal',
                  'type_entreprise', 'adresse']


class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ('username', 'email', 'telephone')
        # fields = ('username', 'email', 'telephone', 'role')
