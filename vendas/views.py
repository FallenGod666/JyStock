from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from estoque.models import Produto, Categoria 
from clientes.models import Cliente
from .models import Venda, ItemVenda

@login_required
def registrar_venda(request):
     
    if request.method == 'POST':
         
        cliente_id = request.POST.get('cliente')
        if not cliente_id:
            messages.error(request, 'Por favor, selecione um cliente.')
            return redirect('registrar_venda')
        try:
            with transaction.atomic():
                cliente = Cliente.objects.get(id=cliente_id)
                nova_venda = Venda.objects.create(cliente=cliente, valor_total=0)
                valor_total_venda = 0
                itens_para_salvar = []
                produtos_para_atualizar = []

                for key, value in request.POST.items():
                    if key.startswith('quantidade-') and value and int(value) > 0:
                        produto_id = key.split('-')[1]
                        quantidade_vendida = int(value)
                        produto = Produto.objects.get(id=produto_id)
                        if produto.quantidade < quantidade_vendida:
                            raise Exception(f"Estoque insuficiente para o produto: {produto.nome}")

                        item = ItemVenda(venda=nova_venda, produto=produto, quantidade=quantidade_vendida, preco_unitario=produto.preco_venda)
                        itens_para_salvar.append(item)
                        valor_total_venda += produto.preco_venda * quantidade_vendida
                        produto.quantidade -= quantidade_vendida
                        produtos_para_atualizar.append(produto)

                if not itens_para_salvar:
                    raise Exception("Nenhum produto foi selecionado para a venda.")

                ItemVenda.objects.bulk_create(itens_para_salvar)
                Produto.objects.bulk_update(produtos_para_atualizar, ['quantidade'])
                nova_venda.valor_total = valor_total_venda
                nova_venda.save()
                messages.success(request, f'Venda #{nova_venda.id} registrada com sucesso!')
                return redirect('registrar_venda')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('registrar_venda')
       
     
    filtro_nome = request.GET.get('nome_produto')
    filtro_categoria = request.GET.get('categoria')

     
    produtos_em_estoque = Produto.objects.filter(quantidade__gt=0).order_by('nome')

    
    if filtro_nome:
        produtos_em_estoque = produtos_em_estoque.filter(nome__icontains=filtro_nome)
    
    if filtro_categoria:
        produtos_em_estoque = produtos_em_estoque.filter(categoria_id=filtro_categoria)

    
    todos_clientes = Cliente.objects.all().order_by('nome_razao_social')
    todas_categorias = Categoria.objects.all().order_by('titulo')
    
    context = {
        'produtos': produtos_em_estoque,
        'clientes': todos_clientes,
        'categorias': todas_categorias, 
    }
    
    return render(request, 'registrar_venda.html', context)