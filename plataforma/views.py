from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from estoque.models import Produto 
#from vendas.models import Venda
#from cupons.models import Cupom


#@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
    
    total_produtos = Produto.objects.count()
    
    total_itens_estoque = Produto.objects.aggregate(
        total=Sum('quantidade')
    )['total'] or 0

    valor_total_estoque = Produto.objects.annotate(
        valor_item=ExpressionWrapper(F('quantidade') * F('preco_venda'), output_field=DecimalField())
    ).aggregate(
        total=Sum('valor_item')
    )['total'] or 0.00

    try:
        produtos_baixo_estoque = Produto.objects.filter(quantidade__gt=0, quantidade__lte=F('estoque_minimo')).count()
    except:
        produtos_baixo_estoque = 0

    produtos_esgotados = Produto.objects.filter(quantidade=0).count()
    cupons_ativos = Cupom.objects.filter(ativo=True).count()

    hoje = timezone.now().date()
    faturamento_hoje = Venda.objects.filter(data__date=hoje).aggregate(total=Sum('valor_total'))['total'] or 0.00

    mes_atual = timezone.now().month
    ano_atual = timezone.now().year
    faturamento_mes = Venda.objects.filter(data__year=ano_atual, data__month=mes_atual).aggregate(total=Sum('valor_total'))['total'] or 0.00
    
    context = {
        'total_produtos': total_produtos,
        'total_itens_estoque': total_itens_estoque,
        'valor_total_estoque': valor_total_estoque,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'produtos_esgotados': produtos_esgotados,
        'cupons_ativos': cupons_ativos,
        'faturamento_hoje': faturamento_hoje,
        'faturamento_mes': faturamento_mes,
    }
    
    return render(request, 'dashboard.html', context)