
from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule


class Offre(models.Model):

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    statut = models.CharField(max_length=20, choices=[
        ('proposee', 'Proposee'),
        ('acceptee', 'Acceptee'),
        ('refusee', 'Refusee'),
        ('retiree', 'Retiree'),
    ], default='proposee')

    date_proposition = models.DateField(auto_now_add=True)

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='Offre'
    )

    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='Offre'
    )

    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='Offre'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if not (
            self.expedition_id
            and self.transporteur_id
            and self.vehicule_id
        ):
            return

        # Regle 1 : entreprise transporteur
        if self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError(
                "L'offre doit être proposée par un transporteur"
            )

        # Regle 2 : vehicule du meme transporteur
        if self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError(
                "Le véhicule doit appartenir au transporteur"
            )

        # Regle 3 : nouvelle offre uniquement si publiee
        if self._state.adding:
            if self.expedition.statut != 'publiee':
                raise ValidationError(
                    "L'expédition doit être publiée"
                )

        # Regle 4 : une seule offre proposee par entreprise
        if self.statut == 'proposee':
            offres = Offre.objects.filter(
                expedition=self.expedition,
                transporteur=self.transporteur,
                statut='proposee'
            ).exclude(pk=self.pk)

            if offres.exists():
                raise ValidationError(
                    "Ce transporteur possède déjà une offre proposée"
                )

        # Regle 6 : vehicule disponible pour une nouvelle offre
        if self._state.adding:
            if not self.vehicule.disponibilite:
                raise ValidationError(
                    "Le véhicule n'est pas disponible"
                )

        # Regle 7 : compatibilite du vehicule
        capacites = {
            'camionnette': 1500,
            'fourgon': 3500,
            'camion_porteur': 19000,
            'semi_remorque': 26000
        }

        capacite_max = capacites.get(
            self.vehicule.type_vehicule, 0
        )

        if self.expedition.poids_kg > self.vehicule.capacite_kg:
            raise ValidationError(
                "Le poids dépasse la capacité du véhicule"
            )

        if self.expedition.poids_kg > capacite_max:
            raise ValidationError(
                "Le type de véhicule est incompatible avec le poids"
            )

        # Regle 5 : verifier l'acceptation
        if self.statut == 'acceptee':

            ancienne = None

            if not self._state.adding:
                ancienne = Offre.objects.filter(
                    pk=self.pk
                ).first()

            if ancienne is None or ancienne.statut != 'acceptee':
                if self.expedition.statut != 'publiee':
                    raise ValidationError(
                        "Cette expédition ne peut plus être attribuée"
                    )

    def save(self, *args, **kwargs):

        with transaction.atomic():

            self.full_clean()

            super().save(*args, **kwargs)

            # Regle 5 : cascade lors de l'acceptation
            if self.statut == 'acceptee':

                Expedition.objects.filter(
                    pk=self.expedition_id
                ).update(statut='attribuee')

                Offre.objects.filter(
                    expedition_id=self.expedition_id,
                    statut='proposee'
                ).exclude(pk=self.pk).update(
                    statut='refusee'
                )
