
from django.urls import path
from produto import views

urlpatterns = [
    path('', views.visualizarLoja, name='shop'),
    path('<slug:categoria_slug>/', views.visualizarLoja, name='produtos_por_categoria'),
    path('<slug:categoria_slug>/<slug:produto_slug>/', views.visualizarDetalheProduto, name='visualizarDetalheProduto'),
]
