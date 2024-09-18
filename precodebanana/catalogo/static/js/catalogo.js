function adicionaprodutoaocarrinho(produtoId) {
    let id_produto = document.getElementById('id_produto_'+produtoId).value;  // Obtém o ID do produto do campo oculto

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
            },
            error: function (response) {
                console.log('Erro ao adicionar produto ao carrinho');
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", function(){
    const procurar = document.getElementById('procurar-input');
    const produtos = Array.from(document.getElementsByClassName('cards-produtos'));
    procurar.addEventListener('input', function(){
        const achados = procurar.value.toLowerCase()
        produtos.forEach(prod =>{
            const nomeProd = prod.querySelector("p:nth-child(1)").textContent.toLowerCase();
            const precoProd = prod.querySelector("p:nth-child(2)").textContent.toLowerCase();
            const precocaixaProd = prod.querySelector("p:nth-child(3)").textContent.toLowerCase();
            if (nomeProd.includes(achados) || precoProd.includes(achados) || precocaixaProd.includes(achados)){
                prod.style.display = 'block';
            }else{
                prod.style.display = 'none';
            }
        })
    })
})

