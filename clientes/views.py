import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente


@login_required
def gerenciar_clientes(request):
    if request.method == 'POST':
        
        try:
            Cliente.objects.create(
                tipo_pessoa=request.POST.get('tipo_pessoa'),
                nome_razao_social=request.POST.get('nome_razao_social'),
                nome_fantasia=request.POST.get('nome_fantasia'),
                cpf_cnpj=request.POST.get('cpf_cnpj'),
                inscricao_estadual=request.POST.get('inscricao_estadual'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                cep=request.POST.get('cep'),
                logradouro=request.POST.get('logradouro'),
                numero=request.POST.get('numero'),
                complemento=request.POST.get('complemento'),
                bairro=request.POST.get('bairro'),
                cidade=request.POST.get('cidade'),
                uf=request.POST.get('uf'),
            )
            messages.success(request, 'Cliente cadastrado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar cliente: {e}')
        
        return redirect('gerenciar_clientes')
        
    clientes = Cliente.objects.all()
    return render(request, 'gerenciar_clientes.html', {'clientes': clientes})


@login_required
def buscar_cnpj(request, cnpj):
    
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    
     
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)