
from django.urls import path
import departamento
from produto import views

urlpatterns = [
    path('', views.visualizarLoja, name='shop'),
    path('departamento/<slug:departamento_slug>/categoria/<slug:categoria_slug>/', views.visualizarLoja, name='produtos_por_categoria'),
    path('departamento/<slug:departamento_slug>/', views.visualizarLoja, name='produtos_por_departamento'),
    path('departamento/<slug:departamento_slug>/categoria/<slug:categoria_slug>/<slug:produto_slug>/', views.visualizarDetalheProduto, name='visualizarDetalheProduto'),
    path('calcular-frete/', views.calcularFrete, name='calcularFrete'),
    path('busca/<str:keyword>/', views.visualizarLoja, name='search_by_keyword'),
    path('busca/', views.visualizarLoja, name='search_base'),


]
