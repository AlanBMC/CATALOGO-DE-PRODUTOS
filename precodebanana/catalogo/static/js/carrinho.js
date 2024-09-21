
function atualizaprecototal(precoporcaixa, quantidade,quantidade_var, precounitario, produtoID) {
    // Atualiza preço total atacado
    const precoTotalAtacado = precoporcaixa * quantidade;
    document.getElementById(`preco-total-${produtoID}`).innerText = 'R$ ' + precoTotalAtacado.toFixed(2);

    // Atualiza preço total varejo
    const precoTotalVarejo = precounitario * quantidade_var;
    document.getElementById(`preco-total-var-${produtoID}`).innerText = 'R$ ' + precoTotalVarejo.toFixed(2);

    atualizaCarrinhoBackend(produtoID, quantidade, quantidade_var)  // Atualiza o backend
    atualizaTotalDosProdutos();
}

function atualizaCarrinhoBackend(produtoID, quantidade, quantidade_var) {
    fetch('/atualiza_carrinho/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Se estiver usando Django com CSRF
        },
        body: JSON.stringify({
            'id_produto': produtoID,
            'quantidade': quantidade,
            'quantidade_var': quantidade_var
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.status);  // Exibe o status da atualização
        const precoTotalElemento = document.getElementById(`preco-total-var-${produtoID}`);
        const precoTotalatacado = document.getElementById(`preco-total-${produtoID}`);
        const total = document.getElementById('total-dos-ff');
        const precototalatacado = parseFloat(data.subtotal).toFixed(2);
        const precoTotal = parseFloat(data.subtotal_var).toFixed(2);  // Subtotal atualizado vindo do backend
        const totalpr = parseFloat(data.total).toFixed(2);
        if (precoTotalElemento) {
            precoTotalElemento.innerText = `R$ ${precoTotal}`;  // Atualiza o texto do preço
        }
        if (precototalatacado){
            precoTotalatacado.innerText = `R$ ${precototalatacado}`;
        }
        if(total){
            total.innerText = `R$ ${totalpr}`
        }
        atualizaTotalDosProdutos();
    })
    .catch(error => {
        console.error('Erro ao atualizar o carrinho:', error);
    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Verifica se esse cookie começa com o nome fornecido
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função que calcula o total dos produtos


function validarInteiro(input) {
    const valor = input.value;
    if (valor === "") {
        return;
    }
    // Verifica se o valor é um número inteiro maior ou igual a 1
    if (!Number.isInteger(parseFloat(valor)) || parseInt(valor) < 1) {
        input.value = 0;  // Se não for válido, redefine para o valor mínimo (1)
    }
}


function atualizaTotalDosProdutos() {
    let totalDosProdutos = 0;
    
    // Itera por todos os elementos de preços atacado e varejo
    document.querySelectorAll('[id^="preco-total-"]').forEach(precoElemento => {
        const precoTexto = precoElemento.innerText.replace('R$', '').trim();
        const preco = parseFloat(precoTexto);
        
        if (!isNaN(preco)) {
            totalDosProdutos += preco;
        }
    });

    // Atualiza o valor total no elemento com id="total-dos-produtos"
    const totalDosProdutosElemento = document.getElementById('total-dos-produtos');
    if (totalDosProdutosElemento) {
        totalDosProdutosElemento.innerText = 'R$ ' + totalDosProdutos.toFixed(2);
    }
}