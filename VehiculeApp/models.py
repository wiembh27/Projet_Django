
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise


class Vehicule(models.Model):

    immatriculation = models.CharField(
        max_length=11,
        unique=True
    )

    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    disponibilite = models.BooleanField(default=True)

    type_vehicule = models.CharField(max_length=20, choices=[
        ('camionnette', 'Camionnette'),
        ('semi_remorque', 'Semi-remorque'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur', 'Camion porteur'),
    ], default='camionnette')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='Vehicule'
    )

    def clean(self):
        if self.entreprise_id:
            if self.entreprise.type_entreprise != 'transporteur':
                raise ValidationError(
                    "Le véhicule doit appartenir à une entreprise transporteur"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.immatriculation