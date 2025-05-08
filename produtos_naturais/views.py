from django.shortcuts import render

from produto.admin import Produto

def home(request):
    produto = Produto.objects.all().filter(esta_disponivel=True)
    
    context = {
        'produto': produto,
    }
    

    return render(request, 'index.html', context)
