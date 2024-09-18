from django.shortcuts import render,redirect, get_object_or_404
from .models import Produto
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import json
import requests
# Create your views here.
def catalogo(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        return render(request, 'catalogo.html',{'catalogo':produtos})

    return render(request, 'catalogo.html')



def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    print(carrinho)
    return render(request, 'carrinho.html', {'produtos': carrinho })


def adiciona_produto_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('id_produto')
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})
        

        carrinho[str(produto_id)]={
            'imagem':str(produto.imagem),
            'nome': produto.nome,
            'preco_por_caixa': float(produto.preco_por_caixa),
            'precoUN': float(produto.preco_un),
            'quantidade_na_caixa': str(produto.quantidade_na_caixa),
            'quantidade': 1
        }    
        request.session['carrinho'] = carrinho
        return JsonResponse({
            'status':'produt adicionado com sucesso'
        })


def remove_produto_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('id_produto')
        carrinho = request.session.get('carrinho', {})
        print('produto id',produto_id)
        # Verifica se o produto está no carrinho e o remove
        if produto_id in carrinho:
            del carrinho[produto_id]  # Remove o produto do carrinho
            request.session['carrinho'] = carrinho  # Atualiza a sessão
            return redirect('carrinho')
        
        else:
            return redirect('carrinho')

    return redirect('carrinho')


def buscacep(request):
    if request.method == 'POST':
        cep = request.POST.get('cep-input')
        cep = cep.replace("-", "").replace(".", "").replace(" ", "")
        print(cep)
        if cep and len(cep) == 8:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                rua = response.json()['logradouro']
                cidade = response.json()['localidade']
                bairro = response.json()['bairro']
                carrinho = request.session.get('carrinho', {})
                return render(request, 'carrinho.html', {'rua': rua,'bairro': bairro,'cidade':cidade, 'produtos': carrinho})
            else:
                print('cep nao encontrado')
                return redirect('carrinho')
        else:
            return redirect('carrinho')
def envia_mensagem_wpp(request):
    if request.method == 'POST':
        rua = request.POST.get('rua')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        complemento = request.POST.get('complemento')
        numero = request.POST.get('numero')
        carrinho = request.session.get('carrinho', {})
        print(rua, complemento, numero)
        return render(request, 'carrinho.html', {'rua': rua,'bairro': bairro,'cidade':cidade, 'produtos': carrinho})
    else:
        return redirect('carrinho')

def processa_e_retorna_dados(cep):
    pass

