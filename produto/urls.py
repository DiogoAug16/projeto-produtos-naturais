
from django.urls import path
import departamento
from produto import views

urlpatterns = [
    path('', views.visualizar_loja, name='shop'),
    path('departamento/<slug:departamento_slug>/categoria/<slug:categoria_slug>/', views.visualizar_loja, name='produtos_por_categoria'),
    path('departamento/<slug:departamento_slug>/', views.visualizar_loja, name='produtos_por_departamento'),
    path('departamento/<slug:departamento_slug>/categoria/<slug:categoria_slug>/<slug:produto_slug>/', views.visualizar_detalhe_produto, name='visualizarDetalheProduto'),
    path('calcular-frete/', views.calcular_frete, name='calcularFrete'),
    path('busca/<str:keyword>/', views.buscar_produtos, name='buscar_produtos'),
]
