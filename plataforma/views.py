from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta
from estoque.models import Produto, Categoria
from vendas.models import Venda
from clientes.models import Cliente

@login_required
def dashboard(request):
    
     
    total_produtos = Produto.objects.count()
    total_itens_estoque = Produto.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    valor_total_estoque = Produto.objects.annotate(
        valor_item=ExpressionWrapper(F('quantidade') * F('preco_venda'), output_field=DecimalField())
    ).aggregate(total=Sum('valor_item'))['total'] or 0.00
    
    produtos_esgotados = Produto.objects.filter(quantidade=0).count()
    
     
    try:
        produtos_baixo_estoque = Produto.objects.filter(quantidade__gt=0, quantidade__lte=F('estoque_minimo')).count()
    except:
        produtos_baixo_estoque = 0  

    
    try:
        
        cupons_ativos = 0  
    except:
        cupons_ativos = 0
    
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    faturamento_hoje = Venda.objects.filter(data__date=hoje).aggregate(total=Sum('valor_total'))['total'] or 0.00
    faturamento_mes = Venda.objects.filter(data__year=ano_atual, data__month=mes_atual).aggregate(total=Sum('valor_total'))['total'] or 0.00

    periodo_filtro = request.GET.get('periodo', 'mes')
    data_atual = timezone.now()

    if periodo_filtro == 'dia':
        data_inicio = data_atual - timedelta(days=6)
        trunc_func = TruncDay
        formato_label = '%d/%m'
    elif periodo_filtro == 'ano':
        data_inicio = data_atual.replace(day=1, month=1)
        trunc_func = TruncMonth
        formato_label = '%m/%Y'
    else:  
        data_inicio = data_atual - timedelta(days=29)
        trunc_func = TruncDay
        formato_label = '%d/%m'

    vendas_agrupadas = Venda.objects.filter(
        data__gte=data_inicio
    ).annotate(
        periodo=trunc_func('data')
    ).values('periodo').annotate(
        total=Sum('valor_total')
    ).order_by('periodo')    
    
    dados_completos = { (data_inicio + timedelta(days=i)).strftime(formato_label) : 0 for i in range((data_atual - data_inicio).days + 1) }
    if periodo_filtro == 'ano':
        dados_completos = { (data_inicio.replace(month=m)).strftime(formato_label) : 0 for m in range(1, data_atual.month + 1) }

    for venda in vendas_agrupadas:
        chave = venda['periodo'].strftime(formato_label)
        dados_completos[chave] = float(venda['total'])

    chart_labels = list(dados_completos.keys())
    chart_data = list(dados_completos.values())

    context = {        
        'total_produtos': total_produtos,
        'total_itens_estoque': total_itens_estoque,
        'valor_total_estoque': valor_total_estoque,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'produtos_esgotados': produtos_esgotados,
        'cupons_ativos': cupons_ativos,
        'faturamento_hoje': faturamento_hoje,
        'faturamento_mes': faturamento_mes,       
         
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'periodo_filtro': periodo_filtro,
    }
    
    return render(request, 'dashboard.html', context)