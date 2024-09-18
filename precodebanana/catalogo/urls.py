from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('adicionar_ao_carrinho/', views.adiciona_produto_carrinho, name='adiciona_produto_carrinho'),
    path('remove_produto_carrinho/', views.remove_produto_carrinho, name='remove_prod_carrinho'),
    path('buscacep/', views.buscacep, name='busca_cep'),
    path('enviaepedido/', views.envia_mensagem_wpp, name='envia_pedido'),
    path('atualiza_carrinho/', views.atualiza_carrinho, name='atualiza_carrinho'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
