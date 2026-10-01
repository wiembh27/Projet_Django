from django.db import models
from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Utilisateur
from VehiculeApp.models import Vehicule


class Offre(models.Model):
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delai_jours = models.PositiveIntegerField()

    statut = models.CharField(
        max_length=20,
        choices=[
            ('proposee', 'Proposee'),
            ('acceptee', 'Acceptee'),
            ('refusee', 'Refusee'),
            ('retiree', 'Retiree'),
        ],
        default='proposee'
    )

    date_proposition = models.DateField(
        auto_now_add=True
    )

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='Offres'
    )

    transporteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='Offres'
    )

    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='Offres'
    )
