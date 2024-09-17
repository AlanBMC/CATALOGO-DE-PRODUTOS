from django.shortcuts import render,redirect, get_object_or_404
from .models import Produto
from django.http import JsonResponse


# Create your views here.
def catalogo(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()

        return render(request, 'catalogo.html',{'catalogo':produtos})

    return render(request, 'catalogo.html')

def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    print(carrinho)
    return render(request, 'carrinho.html')


def adiciona_produto_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('id_produto')
        produto = get_object_or_404(Produto, id=produto_id)
        print(produto.nome)
        carrinho = request.session.get('carrinho', {})
        

        carrinho[str(produto_id)]={
            'imagem':str(produto.imagem),
            'nome': produto.nome,
            'preco_por_caixa': float(produto.preco_por_caixa),
            'precoUN': float(produto.preco_un),
            'quantidade': 1
        }    

        request.session['carrinho'] = carrinho
        return JsonResponse({
            'status':'produt adicionado com sucesso'
        })
def envia_mensagem_wpp(request):
    pass

