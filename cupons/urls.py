from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar/', views.gerenciar_cupons, name='gerenciar_cupons'),
]