from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('carrinho/', views.carrinho, name='carrinho')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
