function adicionaprodutoaocarrinho(produtoId) {
    let id_produto = document.getElementById('id_produto_' + produtoId).value;  // Obtém o ID do produto do campo oculto
    sucesso()
    if (id_produto.trim() !== "") {
        $.ajax({
            url: addprodutoURL,  // Não precisa incluir o ID do produto na URL
            type: 'POST',
            data: {
                'id_produto': id_produto,  // Certifique-se de passar o ID corretamente
                'csrfmiddlewaretoken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // CSRF Token
            },
            success: function (data) {
                console.log('Produto adicionado com sucesso');
                console.log(data)
                document.getElementById('quantidade-produtos-no-carrinho').textContent = data.alertquantidade;
            },
            error: function (response) {
                console.log('Erro ao adicionar produto ao carrinho');
            }
        });
    }
}
function sucesso() {
    var mensagem = document.getElementById('mensagem-sucesso');
    console.log('entrou')
    // Exibir a mensagem
    mensagem.style.display = 'block';
    
    // Após 3 segundos, adicionar a classe de fade-out
    setTimeout(function() {
        mensagem.classList.add('fade-out');
    }, 2000);

    // Após 4 segundos, ocultar a mensagem
    setTimeout(function() {
        mensagem.style.display = 'none';
        mensagem.classList.remove('fade-out'); // Remover a classe de animação
    }, 4000);
}