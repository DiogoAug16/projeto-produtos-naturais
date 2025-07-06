from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
import requests 
import os 

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True) 
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # 1. Primeiro, verifica se o e-mail já existe no seu banco de dados (rápido e grátis)
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
            
        # 2. Se for único, faz a verificação com a API externa
        api_key = os.getenv('EMAIL_API_KEY')
        
        # Só executa se a chave de API estiver configurada
        if api_key:
            try:
                # Monta a URL da API
                url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
                
                # Faz a requisição
                response = requests.get(url)
                
                # Se a requisição for bem-sucedida
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verificamos algumas condições da resposta da API
                    # - É um e-mail descartável?
                    # - A "entregabilidade" é marcada como "UNDELIVERABLE"?
                    if data['is_disposable_email']['value'] or data['deliverability'] == 'UNDELIVERABLE':
                        raise forms.ValidationError("Este endereço de e-mail não é válido ou é temporário.")
                else:
                    # Se a API falhar, podemos registrar o erro mas não bloquear o usuário
                    print(f"Erro ao validar e-mail com a API: {response.status_code}")

            except requests.exceptions.RequestException as e:
                # Se houver um erro de conexão, também não bloqueamos o usuário
                print(f"Erro de conexão ao validar e-mail: {e}")

        # Se todas as validações passarem, retorna o e-mail
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': 'Senha'})
    )