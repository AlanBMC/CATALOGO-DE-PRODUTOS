from django.shortcuts import render
from .models import Produto


# Create your views here.
def catalogo(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()

        return render(request, 'catalogo.html',{'catalogo':produtos})
    return render(request, 'catalogo.html')

def carrinho(request):
    if request.method == 'GET':
        return render(request, 'carrinho.html')
    

def envia_mensagem_wpp(request):
    pass

