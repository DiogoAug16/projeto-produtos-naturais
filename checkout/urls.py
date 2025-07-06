from django.conf import settings
from django.urls import path

from checkout import views


urlpatterns = [
    path('', views.visualizarCheckout, name='checkout'),
]
