function adicionaprodutoaocarrinho(produtoId) {
    let id_produto = document.getElementById('id_produto_' + produtoId).value;  // Obtém o ID do produto do campo oculto

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

