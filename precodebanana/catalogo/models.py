from django.db import models


# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='produtos/')
    preco_un = models.DecimalField(max_digits=10, decimal_places=2)
    preco_por_caixa = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_na_caixa = models.IntegerField()

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.produto.preco_un
        return self.valor_total
