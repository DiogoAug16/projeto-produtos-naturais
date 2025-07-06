from django.conf import settings
from django.shortcuts import *
from django.urls import path

from checkout import views
from .models import Pedido

def pedido_sucesso_view(request, order_id):
    pedido = get_object_or_404(Pedido, id=order_id, user=request.user)
    return render(request, 'loja/pedido_sucesso.html', {'pedido': pedido})

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('sucesso/<int:order_id>/', pedido_sucesso_view, name='pedido_sucesso'),
]
