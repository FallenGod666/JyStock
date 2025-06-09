from django.db import models
from django.core.validators import MinValueValidator

class Cupom(models.Model):
    TIPO_DESCONTO_CHOICES = [
        ('PERCENTUAL', 'Porcentagem (%)'),
        ('FIXO', 'Valor Fixo (R$)'),
    ]

    codigo = models.CharField(max_length=50, unique=True, help_text="Código que o cliente usará (ex: PROMO10)")
    descricao = models.TextField(blank=True, null=True)
    tipo_desconto = models.CharField(max_length=10, choices=TIPO_DESCONTO_CHOICES, default='PERCENTUAL')
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    ativo = models.BooleanField(default=True)
    data_validade = models.DateField(blank=True, null=True, help_text="Deixe em branco para o cupom nunca expirar")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.tipo_desconto == 'PERCENTUAL':
            return f"{self.codigo} ({self.valor_desconto}%)"
        return f"{self.codigo} (R$ {self.valor_desconto})"

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"