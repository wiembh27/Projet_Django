
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from EntrepriseApp.models import Utilisateur, Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from OffreApp.models import Offre


class Command(BaseCommand):
    help = "Creer les donnees de demonstration TransConnect"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 1. Creation des utilisateurs
        utilisateurs = [
            ('demo_chargeur', 'chargeur'),
            ('demo_transporteur1', 'transporteur'),
            ('demo_transporteur2', 'transporteur')
        ]

        for username, role in utilisateurs:
            utilisateur, created = Utilisateur.objects.get_or_create(
                username=username,
                defaults={
                    'email': username + '@gmail.com',
                    'role': role
                }
            )

            if created:
                utilisateur.set_password('TransConnect2026!')
                utilisateur.save()

        chargeur = Utilisateur.objects.get(username='demo_chargeur')
        transporteur1 = Utilisateur.objects.get(username='demo_transporteur1')
        transporteur2 = Utilisateur.objects.get(username='demo_transporteur2')

        # 2. Creation des entreprises
        entreprise_chargeur, _ = Entreprise.objects.get_or_create(
            matricule_fiscal='7654321AAM000',
            defaults={
                'raison_sociale': 'Demo Chargeur SARL',
                'type_entreprise': 'chargeur',
                'adresse': '10 Avenue Habib Bourguiba, Tunis',
                'utilisateur': chargeur
            }
        )

        entreprise_t1, _ = Entreprise.objects.get_or_create(
            matricule_fiscal='7654322AAM000',
            defaults={
                'raison_sociale': 'Demo Transporteur 1',
                'type_entreprise': 'transporteur',
                'adresse': '20 Avenue de la Republique, Ariana',
                'utilisateur': transporteur1
            }
        )

        entreprise_t2, _ = Entreprise.objects.get_or_create(
            matricule_fiscal='7654323AAM000',
            defaults={
                'raison_sociale': 'Demo Transporteur 2',
                'type_entreprise': 'transporteur',
                'adresse': '30 Avenue Farhat Hached, Sousse',
                'utilisateur': transporteur2
            }
        )

        # 3. Creation des vehicules
        vehicule1, _ = Vehicule.objects.get_or_create(
            immatriculation='111TU2026',
            defaults={
                'type_vehicule': 'camionnette',
                'capacite_kg': 1200,
                'disponibilite': True,
                'entreprise': entreprise_t1
            }
        )

        vehicule2, _ = Vehicule.objects.get_or_create(
            immatriculation='222TU2026',
            defaults={
                'type_vehicule': 'fourgon',
                'capacite_kg': 3000,
                'disponibilite': True,
                'entreprise': entreprise_t2
            }
        )

        # 4. Creation des expeditions
        annee = str(timezone.now().year)[-2:]
        date_souhaitee = timezone.localdate() + timedelta(days=14)

        expedition1, _ = Expedition.objects.get_or_create(
            reference='EXP-' + annee + '-00001',
            defaults={
                'ville_depart': 'Tunis',
                'ville_arrivee': 'Sousse',
                'poids_kg': Decimal('800.00'),
                'date_souhaitee': date_souhaitee,
                'description': 'Expedition de demonstration 1',
                'statut': 'publiee',
                'entreprise': entreprise_chargeur
            }
        )

        expedition2, _ = Expedition.objects.get_or_create(
            reference='EXP-' + annee + '-00002',
            defaults={
                'ville_depart': 'Tunis',
                'ville_arrivee': 'Sfax',
                'poids_kg': Decimal('1000.00'),
                'date_souhaitee': date_souhaitee,
                'description': 'Expedition de demonstration 2',
                'statut': 'publiee',
                'entreprise': entreprise_chargeur
            }
        )

        # 5. Creation des offres
        for expedition in [expedition1, expedition2]:

            Offre.objects.get_or_create(
                expedition=expedition,
                transporteur=entreprise_t1,
                defaults={
                    'vehicule': vehicule1,
                    'prix': Decimal('350.00'),
                    'delai_jours': 2,
                    'statut': 'proposee'
                }
            )

            Offre.objects.get_or_create(
                expedition=expedition,
                transporteur=entreprise_t2,
                defaults={
                    'vehicule': vehicule2,
                    'prix': Decimal('420.00'),
                    'delai_jours': 3,
                    'statut': 'proposee'
                }
            )

        # 6. Affichage du resultat
        self.stdout.write(
            self.style.SUCCESS("Donnees de demonstration creees.")
        )

        for expedition in [expedition1, expedition2]:
            self.stdout.write(
                f"\nExpedition : {expedition.reference} - {expedition.statut}"
            )

            for offre in Offre.objects.filter(expedition=expedition):
                self.stdout.write(
                    f"Offre {offre.id} : "
                    f"{offre.transporteur.raison_sociale} - {offre.statut}"
                )
