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
        return render(request, 'catalogo.html',{'catalogo':produtos, 'alertquantidade':quantidade_produtos, 'varejo': False})

    return render(request, 'catalogo.html')


def catalogo_varejo(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        carrinho = request.session.get('carrinho', {})
        quantidade_produtos= len(carrinho)
        return render(request, 'catalogo.html',{'catalogo':produtos, 'alertquantidade':quantidade_produtos, 'varejo': True})

    return render(request, 'catalogo.html')



def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    quantidade_produtos = len(carrinho)
    total = 0
    for item in carrinho.values():
        total += item['subtotal'] + item.get('subtotal_var', 0)
    total = float(total)
    return render(request, 'carrinho.html', {'produtos': carrinho,'alertquantidade': quantidade_produtos, 'total': total})

def adiciona_produto_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('id_produto')
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})

        if str(produto_id) in carrinho:
            # Se o produto já está no carrinho, incrementa a quantidade
            carrinho[str(produto_id)]['quantidade'] += 1
            carrinho[str(produto_id)]['quantidade_var'] += 1
            preco_por_caixa = float(carrinho[str(produto_id)]['preco_por_caixa'])
            preco_varejo = float(carrinho[str(produto_id)]['preco_avulso'])
            quantidade = int(carrinho[str(produto_id)]['quantidade'])
            quantidade_var = int(carrinho[str(produto_id)]['quantidade_var'])
            carrinho[str(produto_id)]['subtotal_var'] = preco_varejo * quantidade_var
            carrinho[str(produto_id)]['subtotal'] = preco_por_caixa * quantidade
        else:
            
            sub = float(produto.preco_avulso) * 5
            carrinho[str(produto_id)] = {
                'imagem': str(produto.imagem),
                'nome': produto.nome,
                'preco_por_caixa': float(produto.preco_por_caixa),
                'precoUN': float(produto.preco_un),
                'quantidade_na_caixa': str(produto.quantidade_na_caixa),
                'preco_avulso': float(produto.preco_avulso),
                'quantidade': 1,
                'quantidade_var': 5,
                'subtotal_var':sub,
                'subtotal': float(produto.preco_por_caixa)
             
            }
        request.session['carrinho'] = carrinho
        carrinho = request.session.get('carrinho', {})
        carrinho_quantidade = len(carrinho)
        return JsonResponse({
            'status':'produt adicionado com sucesso',
            'alertquantidade':carrinho_quantidade
        })

def atualiza_carrinho(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = data.get('id_produto')
        quantidade = data.get('quantidade') 
        quantidade_var = data.get('quantidade_var') 
        # Pega o carrinho da sessão
        carrinho = request.session.get('carrinho', {})

        if str(produto_id) in carrinho:
            # Converte preco_por_caixa e quantidade para float/int
            preco_por_caixa = float(carrinho[str(produto_id)]['preco_por_caixa'])
            quantidade = int(quantidade)
            preco_avulso = float(carrinho[str(produto_id)]['preco_avulso'])
            quantidade_var = int(quantidade_var)
            # Atualiza o subtotal do produto
            carrinho[str(produto_id)]['subtotal'] = preco_por_caixa * quantidade
            carrinho[str(produto_id)]['subtotal_var'] = preco_avulso * quantidade_var
            # Atualiza a quantidade do produto no carrinho
            carrinho[str(produto_id)]['quantidade'] = quantidade
            carrinho[str(produto_id)]['quantidade_var'] = quantidade_var
            # Salva o carrinho atualizado na sessão
            request.session['carrinho'] = carrinho
            total = 0
            for item in carrinho.values():
                total += item['subtotal'] + item['subtotal_var']
            return JsonResponse({'status': 'Carrinho atualizado com sucesso', 
                                 'subtotal': carrinho[str(produto_id)]['subtotal'],
                                'subtotal_var': carrinho[str(produto_id)]['subtotal_var'],
                                'total': total})
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

        # Obtendo o carrinho da sessão
        carrinho = request.session.get('carrinho', {})
        total_geral = 0
        mensagem_produto = ''

        for item in carrinho.values():
            # Cálculos individuais
            preco_total_atacado = item['subtotal']
            preco_total_varejo = item['subtotal_var']
            quantidade_por_caixa = item['quantidade_na_caixa']
            quantidade_atacado = item['quantidade']
            quantidade_varejo = item['quantidade_var']

            # Acumula o total geral
            total_geral += preco_total_atacado + preco_total_varejo

            # Formata a mensagem detalhada do produto
            mensagem_produto += f'''Produto: {item['nome']}
Quantidade pedida no Atacado (caixas): {quantidade_atacado}
Quantidade por Caixa: {quantidade_por_caixa}
Preço Total no Atacado: R$ {preco_total_atacado:.2f}

Quantidade pedida no Varejo: {quantidade_varejo}
Preço Total no Varejo: R$ {preco_total_varejo:.2f}

-----------------------------------
'''

        # Monta a mensagem final com o total dos produtos e o frete (se necessário)
        mensagem = f'''--- RESUMO DO PEDIDO ---
Total dos Produtos (sem frete): R$ {total_geral:.2f}
Total com Frete: A combinar
---------------------------
{mensagem_produto}'''

        # Codifica a mensagem e cria a URL do WhatsApp
        mensagem_encoded = urllib.parse.quote(mensagem)
        numero_telefone = "+5565981488445".replace('+', '')
        whatsapp_url = f"https://wa.me/{numero_telefone}?text={mensagem_encoded}"

        
        
        return redirect(whatsapp_url)
        #return render(request, 'carrinho.html', {'produtos': carrinho, 'alertquantidade':len(carrinho)})
    else:
        return redirect('carrinho')


