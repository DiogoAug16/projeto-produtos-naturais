
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static  

from favoritos import views

urlpatterns = [
    path('', views.visualizarFavorito, name='favoritos'),
    path('adicionar_favorito/<int:produto_id>/', views.adicionarItemFavorito, name='adicionarFavorito'),
    path('diminuir_qtde_favorito/<int:produto_id>/', views.diminuirQuantidadeProdutoFavorito, name='diminuirQuantidadeProdutoFavorito'),
    path('removerItemFavorito/<int:produto_id>/', views.removerItemFavorito, name='removerItemFavorito'),


]
