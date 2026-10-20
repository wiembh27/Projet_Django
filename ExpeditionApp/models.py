
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from EntrepriseApp.models import Entreprise


class Expedition(models.Model):

    reference = models.CharField(
        max_length=20,
        unique=True
    )

    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)

    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    date_souhaitee = models.DateField()
    description = models.TextField(blank=True)

    statut = models.CharField(max_length=20, choices=[
        ('publiee', 'Publiee'),
        ('attribuee', 'Attribuee'),
        ('en_cours', 'En cours'),
        ('livree', 'Livree'),
        ('annulee', 'Annulee'),
    ], default='publiee')

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='Expedition'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.entreprise_id:
            if self.entreprise.type_entreprise != 'chargeur':
                raise ValidationError(
                    "L'expédition doit appartenir à une entreprise chargeur"
                )

    def save(self, *args, **kwargs):

        if not self.reference:
            annee = str(timezone.now().year)[-2:]
            prefixe = 'EXP-' + annee + '-'

            derniere = Expedition.objects.filter(
                reference__startswith=prefixe
            ).order_by('-reference').first()

            if derniere:
                numero = int(derniere.reference[-5:]) + 1
            else:
                numero = 1

            if numero > 99999:
                raise ValidationError(
                    "Nombre maximum d'expéditions atteint pour cette année"
                )

            self.reference = prefixe + str(numero).zfill(5)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference