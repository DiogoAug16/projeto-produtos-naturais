
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static  

from carrinho import views

urlpatterns = [
    path('', views.visualizarCarrinho, name='carrinho'),
    path('adicionar_carrinho/<int:produto_id>/', views.adicionarItemCarrinho, name='adicionarCarrinho'),
    path('diminuir_qtde_carrinho/<int:produto_id>/', views.diminuirQuantidadeProdutoCarrinho, name='diminuirQuantidadeProdutoCarrinho'),
    path('removerItemCarrinho/<int:produto_id>/', views.removerItemCarrinho, name='removerItemCarrinho'),


]
