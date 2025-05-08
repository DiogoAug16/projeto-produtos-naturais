
from django.urls import path
from produto import views

urlpatterns = [
    path('', views.visualizarLoja, name='shop'),
    path('<slug:categoria_slug>/', views.visualizarLoja, name='produtos_por_categoria'),
]
