from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        
        fields = [
            'nome', 'sobrenome', 'endereco', 'numero_endereco', 
            'complemento_endereco', 'estado', 'cidade', 'cep', 
            'telefone', 'cpf', 'metodo_pagamento'
        ]