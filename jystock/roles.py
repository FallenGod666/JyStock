import importlib
from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
        'liberar_descontos': True,
        'cadastrar_vendedor': True,
        'realizar_venda': True,
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'realizar_venda': True,
        'cadastrar_produtos': True,
        'cadastrar_vendedor': True,
    }