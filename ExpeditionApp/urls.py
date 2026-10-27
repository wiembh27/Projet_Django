from django.urls import path
from .views import *
app_name="expedition"
urlpatterns = [
    path('home/', home, name="home"),
    path('welcome/<str:name>/', welcome, name="welcome"),
    path('list/', listExpeditions, name="list"),
    path('details/<int:pk>/', detailsExpedition, name="details"),
    path('delete/<int:pk>/', deleteExpedition, name="delete"),
]

# Python est organisé de manière séquentielle.
# Django parcourt les routes dans l'ordre et utilise la première qui correspond à l'URL demandée.