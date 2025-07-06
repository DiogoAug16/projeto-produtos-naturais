from django.conf import settings
from django.shortcuts import *
from django.urls import path

from checkout import views
from .models import Pedido

urlpatterns = [
    path('', view=views.checkout_view, name='checkout'),
]
