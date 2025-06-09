from django.db import models
from django.conf import settings 
from estoque.models import Produto

class Venda(models.Model):    
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Venda #{self.id} - {self.data.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"


class ItemVenda(models.Model):    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} na Venda #{self.venda.id}"

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"