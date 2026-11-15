
from django.urls import path
from . import views

app_name = 'expedition'

urlpatterns = [
    path('', views.listExpeditions, name='liste'),

    path('home/', views.home, name='home'),

    path('welcome/<str:name>/', views.welcome, name='welcome'),

    path('list/', views.listExpeditions, name='list'),

    path(
        'details/<int:pk>/',
        views.detailsExpedition,
        name='details'
    ),

    path(
        'delete/<int:pk>/',
        views.deleteExpedition,
        name='delete'
    ),

    path(
        '<str:reference>/',
        views.detail_expedition_reference,
        name='detail'
    ),
]
