
function atualizaprecototal(precoporcaixa, quantidade, precototalid, produtoID){
    const precototal = precoporcaixa * quantidade;
    const precototalfomatado = precototal.toFixed(3)
    document.getElementById(precototalid).innerText = 'R$ ' + precototalfomatado
    
    totaldosprodutos()
    atualizaCarrinhoBackend(produtoID, quantidade);
}
function atualizaCarrinhoBackend(produtoID, quantidade) {
    fetch('/catalogo/atualiza_carrinho/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Se estiver usando Django com CSRF
        },
        body: JSON.stringify({
            'id_produto': produtoID,
            'quantidade': quantidade
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.status);  // Exibe o status da atualização
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

function totaldosprodutos(){
    let totalGeral = 0;
    const precostotais = document.querySelectorAll('[id^="preco-total-"')
    precostotais.forEach(function(precoElemento){
        const preco = parseFloat(precoElemento.innerText.replace('R$', '').replace(',', '.'));
        totalGeral += preco
    })
    document.getElementById('total-dos-produtos').innerText = 'R$ ' + totalGeral.toFixed(3)
    document.getElementById('total-com-frete').innerText = 'R$ ' + totalGeral.toFixed(3)
    document.getElementById('totalfrete').value = totalGeral.toFixed(3)
    document.getElementById('totalpreco').value = totalGeral.toFixed(3)
}
document.addEventListener('DOMContentLoaded', function() {
    totaldosprodutos();  // Calcula o total dos produtos logo quando a página é carregada
});

function validarInteiro(input) {
    const valor = input.value;
    if (valor === "") {
        return;
    }
    // Verifica se o valor é um número inteiro maior ou igual a 1
    if (!Number.isInteger(parseFloat(valor)) || parseInt(valor) < 1) {
        input.value = 1;  // Se não for válido, redefine para o valor mínimo (1)
    }
}
