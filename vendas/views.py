from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from estoque.models import Produto, Categoria
from clientes.models import Cliente
from cupons.models import Cupom
from .models import Venda, ItemVenda

@login_required
def registrar_venda(request):    
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        codigo_cupom = request.POST.get('codigo_cupom', '').upper().strip()

        if not cliente_id:
            messages.error(request, 'Erro: Por favor, selecione um cliente.')
            return redirect('registrar_venda')

        try:            
            with transaction.atomic():
                cliente = Cliente.objects.get(id=cliente_id)                
                
                nova_venda = Venda.objects.create(cliente=cliente)
                
                valor_total_bruto = Decimal('0.0')
                itens_para_salvar = []
                produtos_para_atualizar = []

                
                for key, value in request.POST.items():
                    if key.startswith('quantidade-') and value and int(value) > 0:
                        produto_id = int(key.split('-')[1])
                        quantidade_vendida = int(value)
                        
                        produto = Produto.objects.select_for_update().get(id=produto_id) 

                        if produto.quantidade < quantidade_vendida:
                            raise Exception(f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.quantidade}.")

                        valor_item_total = produto.preco_venda * quantidade_vendida
                        valor_total_bruto += valor_item_total

                        item = ItemVenda(
                            venda=nova_venda,
                            produto=produto,
                            quantidade=quantidade_vendida,
                            preco_unitario=produto.preco_venda
                        )
                        itens_para_salvar.append(item)
                        
                        produto.quantidade -= quantidade_vendida
                        produtos_para_atualizar.append(produto)
                
                if not itens_para_salvar:
                    raise Exception("Nenhum produto foi adicionado à venda.")

                
                desconto_aplicado = Decimal('0.0')
                cupom_obj = None
                if codigo_cupom:
                    try:
                        cupom_obj = Cupom.objects.get(codigo=codigo_cupom, ativo=True)
                        if cupom_obj.data_validade and cupom_obj.data_validade < timezone.now().date():
                            raise Exception("Cupom expirado.")

                        if cupom_obj.tipo_desconto == 'PERCENTUAL':
                            desconto_aplicado = valor_total_bruto * (cupom_obj.valor_desconto / Decimal('100'))
                        else: 
                            desconto_aplicado = cupom_obj.valor_desconto
                        
                        desconto_aplicado = min(valor_total_bruto, desconto_aplicado)
                        messages.success(request, f"Cupom '{cupom_obj.codigo}' aplicado com sucesso!")

                    except Cupom.DoesNotExist:
                        messages.warning(request, f"Cupom '{codigo_cupom}' é inválido ou está inativo.")                
                
                ItemVenda.objects.bulk_create(itens_para_salvar)
                Produto.objects.bulk_update(produtos_para_atualizar, ['quantidade'])                
                
                nova_venda.valor_total = valor_total_bruto - desconto_aplicado
                nova_venda.cupom = cupom_obj
                nova_venda.desconto_aplicado = desconto_aplicado
                nova_venda.save()

                messages.success(request, f'Venda #{nova_venda.id} registrada com o valor de R$ {nova_venda.valor_total:.2f}.')
                return redirect('registrar_venda')

        except Produto.DoesNotExist:
            messages.error(request, "Erro: Um dos produtos selecionados não existe mais.")
        except Exception as e:
            messages.error(request, f"Erro ao processar a venda: {e}")
        
        return redirect('registrar_venda')
    
    else:
        filtro_nome = request.GET.get('nome_produto')
        filtro_categoria = request.GET.get('categoria')

        produtos = Produto.objects.filter(quantidade__gt=0).order_by('nome')

        if filtro_nome:
            produtos = produtos.filter(nome__icontains=filtro_nome)
        
        if filtro_categoria:
            produtos = produtos.filter(categoria_id=filtro_categoria)

        clientes = Cliente.objects.all().order_by('nome_razao_social')
        categorias = Categoria.objects.all().order_by('titulo')
        
        context = {
            'produtos': produtos,
            'clientes': clientes,
            'categorias': categorias,
        }
        return render(request, 'registrar_venda.html', context)