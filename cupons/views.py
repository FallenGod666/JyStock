from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cupom

def is_manager_or_superuser(user):
    return user.is_superuser or user.groups.filter(name='Gerente').exists()

@login_required
@user_passes_test(is_manager_or_superuser, login_url='/dashboard/') 
def gerenciar_cupons(request):
    if request.method == 'POST':
        try:
            Cupom.objects.create(
                codigo=request.POST.get('codigo').upper(),
                descricao=request.POST.get('descricao'),
                tipo_desconto=request.POST.get('tipo_desconto'),
                valor_desconto=request.POST.get('valor_desconto'),
                ativo=request.POST.get('ativo') == 'on',
                data_validade=request.POST.get('data_validade') or None
            )
            messages.success(request, 'Cupom criado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar cupom: {e}')
        return redirect('gerenciar_cupons')

    cupons = Cupom.objects.all().order_by('-data_criacao')
    context = {'cupons': cupons}
    return render(request, 'gerenciar_cupons.html', context)