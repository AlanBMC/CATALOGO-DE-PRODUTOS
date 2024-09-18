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

