
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static  

from favoritos import views

urlpatterns = [
    path('', views.visualizarFavorito, name='favoritos'),
    path('remover_item_favorito/<int:produto_id>/', views.removerItemFavorito, name='removerItemFavorito'),
    path('remover_todos/', views.removerTodosFavoritos, name='removerTodosFavoritos'),
    path('toggle_favorito/<int:produto_id>/', views.toggleFavorito, name='toggleFavorito'),
]
