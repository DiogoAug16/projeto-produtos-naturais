from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegistroForm
from django.contrib import messages

from carrinho.models import Carrinho, CarItem
from favoritos.models import Favoritos, FavItem

def registro(request):
    error_messages = []
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso! Faça o login para continuar.')
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    error_messages.append(f"{field.label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(error)
    else:
        form = RegistroForm()

    return render(request, 'loja/login.html', {
        'form': AuthenticationForm(),
        'registro_form': form,
        'registro_errors': error_messages 
    })
    
def deslogar(request):
    logout(request)
    return redirect('home')

class CustomLoginView(auth_views.LoginView):
    template_name = 'loja/login.html'
    form_class = LoginForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registro_form'] = RegistroForm()
        context['registro_errors'] = []
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha inválidos. Por favor, tente novamente.')
        
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """
        Esta função é chamada após o login ser validado.
        Aqui vamos unir os carrinhos e favoritos da sessão com os do usuário.
        """
        # Primeiro, faz o login normalmente
        response = super().form_valid(form)
        
        try:
            # Pega o carrinho da sessão (se existir)
            session_cart = Carrinho.objects.get(car_id=self.request.session.session_key)
            user_cart, _ = Carrinho.objects.get_or_create(user=self.request.user)
            
            # Move os itens do carrinho da sessão para o carrinho do usuário
            for item in CarItem.objects.filter(carrinho=session_cart):
                # Verifica se o item já existe no carrinho do usuário
                existing_item, created = CarItem.objects.get_or_create(
                    carrinho=user_cart,
                    produto=item.produto
                )
                if not created:
                    # Se já existe, apenas soma a quantidade
                    existing_item.quantidade += item.quantidade
                    existing_item.save()
                else:
                    # Se não existe, move o item para o carrinho do usuário
                    item.carrinho = user_cart
                    item.save()
            
            # Apaga o carrinho antigo da sessão
            session_cart.delete()
        except Carrinho.DoesNotExist:
            pass

        # Lógica de união dos favoritos (idêntica à do carrinho)
        try:
            session_favs = Favoritos.objects.get(fav_id=self.request.session.session_key)
            user_favs, _ = Favoritos.objects.get_or_create(user=self.request.user)
            
            for item in FavItem.objects.filter(favoritos=session_favs):
                item.favoritos = user_favs
                item.save()
            
            session_favs.delete()
        except Favoritos.DoesNotExist:
            pass

        return response
    
