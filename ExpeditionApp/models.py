from django.db import models
from EntrepriseApp.models import Entreprise


class Expedition(models.Model):
    reference = models.CharField(
        max_length=20,
        unique=True
    )

    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    statut = models.CharField(
        max_length=20,
        choices=[
            ('publiee', 'Publiee'),
            ('attribuee', 'Attribuee'),
            ('en_cours', 'En_cours'),
            ('livree', 'Livree'),
            ('annulee', 'Annulee'),
        ],
        default='publiee'
    )

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='Expedition'
    )