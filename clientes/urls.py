from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar/', views.gerenciar_clientes, name='gerenciar_clientes'),
    
    path('buscar-cnpj/<str:cnpj>/', views.buscar_cnpj, name='buscar_cnpj'),
]