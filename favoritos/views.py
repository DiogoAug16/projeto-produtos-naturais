# favoritos/views.py
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from produto.models import Produto

def _get_or_create_favoritos(request):
    if request.user.is_authenticated:
        favoritos, _ = Favoritos.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        favoritos, _ = Favoritos.objects.get_or_create(fav_id=session_key)
    return favoritos

def visualizarFavorito(request):
    fav_items = []
    try:
        favoritos = _get_or_create_favoritos(request)
        fav_items = FavItem.objects.filter(favoritos=favoritos, esta_disponivel=True)
    except Favoritos.DoesNotExist:
        pass
    
    context = {'fav_items': fav_items}
    return render(request, 'loja/shop-favorite.html', context)

def toggleFavorito(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    favoritos = _get_or_create_favoritos(request)
    
    fav_item, created = FavItem.objects.get_or_create(favoritos=favoritos, produto=produto)
    if not created:
        fav_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'favoritos'))

def removerItemFavorito(request, produto_id):
    favoritos = _get_or_create_favoritos(request)
    produto = get_object_or_404(Produto, id=produto_id)
    FavItem.objects.filter(favoritos=favoritos, produto=produto).delete()
    return redirect('favoritos')

def removerTodosFavoritos(request):
    favoritos = _get_or_create_favoritos(request)
    FavItem.objects.filter(favoritos=favoritos).delete()
    return redirect('favoritos')