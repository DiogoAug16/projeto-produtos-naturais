from django.shortcuts import get_object_or_404, redirect, render

from django.core.exceptions import ObjectDoesNotExist

from favoritos.models import *
from produto.models import Produto

# Create your views here.

def getFavId(request):
    favSession = request.session.session_key
    if not favSession:
        favSession = request.session.create()
        favSession = request.session.session_key
    return favSession

def visualizarFavorito(request, fav_items = None, quantidade = 0):
    try:
        fav = Favoritos.objects.get(fav_id = getFavId(request))
        fav_items = FavItem.objects.filter(favoritos = fav, esta_disponivel = True)
        for item in fav_items:
            quantidade += item.quantidade

    except ObjectDoesNotExist:
        pass
    
    context = {
        'fav_items': fav_items,
    }
    
    return render(request, 'shop-favorite.html', context)

def adicionarItemFavorito(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    try:
        favoritos = Favoritos.objects.get(fav_id = getFavId(request))
    except Favoritos.DoesNotExist:
        favoritos = Favoritos.objects.create(
            fav_id = getFavId(request)
        )
    favoritos.save()

    try:
        fav_item = FavItem.objects.get(produto=produto, favoritos=favoritos)
        fav_item.save()
    except FavItem.DoesNotExist:
        fav_item = FavItem.objects.create(
            produto = produto,
            favoritos=favoritos,
        )
        fav_item.save()
    return redirect('favoritos')

def removerItemFavorito(request, produto_id):
    try:
        fav = Favoritos.objects.get(fav_id=getFavId(request))
        produto = get_object_or_404(Produto, id=produto_id)
        fav_item = FavItem.objects.get(produto=produto, favoritos=fav)
        fav_item.delete()
    except (Favoritos.DoesNotExist, FavItem.DoesNotExist):
        pass
    return redirect('favoritos')

def removerTodosFavoritos(request):
    try:
        fav = Favoritos.objects.get(fav_id=getFavId(request))
        FavItem.objects.filter(favoritos=fav).delete()
    except Favoritos.DoesNotExist:
        pass
    return redirect('favoritos')
