from django.contrib.auth import views as auth_views
from django.urls import path

from login_usuario import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('registro/', views.registro, name='registro'),
]
