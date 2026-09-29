from django.db import models

# Create your models here.

class Expedition(models.Model):
    reference=models.CharField(max_length=20, unique=True)
    poid_kg=models.DecimalField()
    status=models.CharField(max_length=20, choices = [
        ('publiee', 'Publiee'),
        ('attribuee', 'Attribuee'), 
        ('en_cour', 'En_cour'),
        ('annulee', 'Annulee'),
        ('livree', 'Livree'),  


    ], default='publiee')


    proprietaire=models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='Expedition')