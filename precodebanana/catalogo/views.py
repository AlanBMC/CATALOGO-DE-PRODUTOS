from django.shortcuts import render,redirect, get_object_or_404
from .models import Produto
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import json
import urllib.parse


# Create your views here.
def catalogo(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        carrinho = request.session.get('carrinho', {})
        quantidade_produtos= len(carrinho)
        return render(request, 'catalogo.html',{'catalogo':produtos, 'alertquantidade':quantidade_produtos})

    return render(request, 'catalogo.html')

def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    quantidade_produtos = len(carrinho)
    return render(request, 'carrinho.html', {'produtos': carrinho,'alertquantidade': quantidade_produtos})

def adiciona_produto_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('id_produto')
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})

        if str(produto_id) in carrinho:
            # Se o produto já está no carrinho, incrementa a quantidade
            carrinho[str(produto_id)]['quantidade'] += 1
        else:

            
            carrinho[str(produto_id)] = {
                'imagem': str(produto.imagem),
                'nome': produto.nome,
                'preco_por_caixa': float(produto.preco_por_caixa),
                'precoUN': float(produto.preco_un),
                'quantidade_na_caixa': str(produto.quantidade_na_caixa),
                'quantidade': 1,
                'subtotal': float(produto.preco_por_caixa) 
            }
        request.session['carrinho'] = carrinho
        carrinho = request.session.get('carrinho', {})
        carrinho_qunatidade = len(carrinho)
        print(carrinho_qunatidade)
        return JsonResponse({
            'status':'produt adicionado com sucesso',
            'alertquantidade':carrinho_qunatidade
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
        # Verifica se o produto está no carrinho e o remove
        if produto_id in carrinho:
            del carrinho[produto_id]  # Remove o produto do carrinho
            request.session['carrinho'] = carrinho  # Atualiza a sessão
            return redirect('carrinho')
        
        else:
            return redirect('carrinho')

    return redirect('carrinho')



def envia_mensagem_wpp(request):
    if request.method == 'POST':

        #total_com_frete = request.POST.get('total-com-frete')
        total_dos_produtos = request.POST.get('total-dos-produtos')
        carrinho = request.session.get('carrinho', {})
        quantidade_produtos = len(carrinho)
 
        
        mensagem = f'''--- PEDIDOS -----
Total dos produtos: {str(total_dos_produtos)}
Total com frete: {str(total_dos_produtos)}
Quantidade de produtos por caixa: {quantidade_produtos}
---------------------------
'''
        mensagem_produto = ''
        for item in carrinho.values():
            preco_total_produto = item['subtotal']
            preco_formatado = preco_total_produto
            mensagem_produto += f"Produto: {item['nome']}, Quantidade por caixa: {item['quantidade']}, Preço: {str(preco_formatado)}\n"

        mensagem += mensagem_produto
        print(mensagem)
        mensagem_encoded = urllib.parse.quote(mensagem)
        numero_telefone = "+5565981488445".replace('+', '')
        whatsapp_url = f"https://wa.me/{numero_telefone}?text={mensagem_encoded}"
        return redirect(whatsapp_url)
        #return render(request, 'carrinho.html', {'produtos': carrinho, 'alertquantidade':len(carrinho)})
    else:
        return redirect('carrinho')


