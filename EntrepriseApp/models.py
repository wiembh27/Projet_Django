
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def valider_gmail(value):
    if not value.lower().endswith('@gmail.com'):
        raise ValidationError("L'email doit appartenir au domaine gmail.com")


valider_matricule = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format du matricule fiscal invalide"
)


class Utilisateur(AbstractUser):

    user_id = models.CharField(max_length=8, primary_key=True)

    email = models.EmailField(
        unique=True,
        validators=[valider_gmail]
    )

    telephone = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    role = models.CharField(max_length=20, choices=[
        ('admin', 'Administrateur'),
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
    ], default='chargeur')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.user_id:
            annee = str(timezone.now().year)[-2:]
            prefixe = annee + 'user'

            dernier = Utilisateur.objects.filter(
                user_id__startswith=prefixe
            ).order_by('-user_id').first()

            if dernier:
                numero = int(dernier.user_id[-2:]) + 1
            else:
                numero = 0

            if numero > 99:
                raise ValidationError(
                    "Nombre maximum d'utilisateurs atteint pour cette année"
                )

            self.user_id = prefixe + str(numero).zfill(2)

        if self.email:
            valider_gmail(self.email)

        super().save(*args, **kwargs)


class Entreprise(models.Model):

    raison_sociale = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    matricule_fiscal = models.CharField(
    max_length=17,
    unique=True,
    validators=[valider_matricule]
)

    type_entreprise = models.CharField(max_length=100, choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
    ], default='chargeur')

    adresse = models.TextField(
        validators=[MinLengthValidator(20)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='entreprise'
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.raison_sociale