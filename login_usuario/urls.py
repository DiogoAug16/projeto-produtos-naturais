from django.contrib.auth import views as auth_views
from django.urls import path
from .views import registro

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', registro, name='registro'),
]
