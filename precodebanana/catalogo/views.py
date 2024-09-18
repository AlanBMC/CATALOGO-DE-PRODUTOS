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

        if str(produto_id) in carrinho:
            # Se o produto já está no carrinho, incrementa a quantidade
            carrinho[str(produto_id)]['quantidade'] += 1
        else:
            # Caso contrário, adiciona o produto ao carrinho
            carrinho[str(produto_id)] = {
                'imagem': str(produto.imagem),
                'nome': produto.nome,
                'preco_por_caixa': float(produto.preco_por_caixa),
                'precoUN': float(produto.preco_un),
                'quantidade_na_caixa': str(produto.quantidade_na_caixa),
                'quantidade': 1,
                'subtotal': 0
            }
        request.session['carrinho'] = carrinho
        return JsonResponse({
            'status':'produt adicionado com sucesso'
        })



def atualiza_carrinho(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = data.get('id_produto')
        quantidade = data.get('quantidade')

        # Pega o carrinho da sessão
        carrinho = request.session.get('carrinho', {})

        if str(produto_id) in carrinho:
            # Converte preco_por_caixa e quantidade para float/int
            preco_por_caixa = float(carrinho[str(produto_id)]['preco_por_caixa'])
            quantidade = int(quantidade)

            # Atualiza o subtotal do produto
            carrinho[str(produto_id)]['subtotal'] = preco_por_caixa * quantidade

            # Atualiza a quantidade do produto no carrinho
            carrinho[str(produto_id)]['quantidade'] = quantidade

            # Salva o carrinho atualizado na sessão
            request.session['carrinho'] = carrinho

            return JsonResponse({'status': 'Carrinho atualizado com sucesso'})
        else:
            return JsonResponse({'status': 'Produto não encontrado no carrinho'}, status=404)

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

        carrinho = request.session.get('carrinho', {})
        return render(request, 'carrinho.html', {'produtos': carrinho})
    else:
        return redirect('carrinho')


