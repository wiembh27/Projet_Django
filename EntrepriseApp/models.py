from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Utilisateur(AbstractUser):
    user_id=models.CharField(max_length=8, 
    primary_key=True) #pas la peine de mettre unqiue car on l a mis en  primary key donc par defaut c est unique
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=15, null=True, blank=True)
    role=models.CharField(max_length=20, choices=[
        ('administrateur', 'Administrateur'),
        ('chargeur', 'Chargeur'), 
        ('transporteur', 'Transporteur'), 
    ], default='chargeur'
    ) 
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Entreprise(models.Model):
    raison_sociale=models.CharField(max_length=200, null=False, blank=False)
    matricule_fiscale=models.CharField(max_length=17, unique=True)
    type_entreprise=models.CharField(max_length=100, choices=[
        ('chargeur', 'Chargeur'), #cle-valeur on peut mettre char et Chargeur
        ('transporteur', 'Transporteur'), #on peut mettre des valeurs differentes ca gene pas on peux meme mettre 1 et 2


    ], default='chargeur' # dans default on met la key pas la valeur
    ) 
    adresse=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    gerant= models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')