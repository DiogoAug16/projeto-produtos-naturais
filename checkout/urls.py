from django.conf import settings
from django.shortcuts import *
from django.urls import path

from checkout import views

urlpatterns = [
    path('', view=views.visualizarCheckout, name='checkout'),
]
