# Generated by Django 5.2.2 on 2025-06-09 23:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cupom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='Código que o cliente usará (ex: PROMO10)', max_length=50, unique=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('tipo_desconto', models.CharField(choices=[('PERCENTUAL', 'Porcentagem (%)'), ('FIXO', 'Valor Fixo (R$)')], default='PERCENTUAL', max_length=10)),
                ('valor_desconto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('ativo', models.BooleanField(default=True)),
                ('data_validade', models.DateField(blank=True, help_text='Deixe em branco para o cupom nunca expirar', null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cupom',
                'verbose_name_plural': 'Cupons',
            },
        ),
    ]
