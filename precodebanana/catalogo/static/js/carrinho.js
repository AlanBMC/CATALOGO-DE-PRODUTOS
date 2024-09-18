function atualizaprecototal(precoporcaixa, quantidade, precototalid){
    const precototal = precoporcaixa * quantidade;
    const precototalfomatado = precototal.toFixed(2)
    console.log(precototalfomatado)
    document.getElementById(precototalid).innerText = 'R$ ' + precototalfomatado
    totaldosprodutos()
}
function totaldosprodutos(){
    let totalGeral = 0;
    const precostotais = document.querySelectorAll('[id^="preco-total-"')
    precostotais.forEach(function(precoElemento){
        const preco = parseFloat(precoElemento.innerText.replace('R$', '').replace(',', '.'));
        totalGeral += preco
    })
    document.getElementById('total-dos-produtos').innerText = 'R$ ' + totalGeral.toFixed(2)
    document.getElementById('total-com-frete').innerText = 'R$ ' + totalGeral.toFixed(2)
}
document.addEventListener('DOMContentLoaded', function() {
    totaldosprodutos();  // Calcula o total dos produtos logo quando a página é carregada
});

function validarInteiro(input) {
    const valor = input.value;
    
    // Verifica se o valor é um número inteiro maior ou igual a 1
    if (!Number.isInteger(parseFloat(valor)) || parseInt(valor) < 1) {
        input.value = 1;  // Se não for válido, redefine para o valor mínimo (1)
    }
}

function buscacep(){
    const cep = document.getElementById('cep').value
    if (cep.trim() !== ""){
        $.ajax({
            url: cepURL,
            Type: 'POST',
            data: {
                'cep':cep,
                'csrfmiddlewaretoken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // CSRF Token

            },
            success: function (data) {
                console.log('achado com sucesso');
            },
            error: function (response) {
                console.log('Erro ao buscar cep');
            }
        })
    }
}