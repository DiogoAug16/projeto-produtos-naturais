from django.shortcuts import get_object_or_404, redirect, render

from django.core.exceptions import ObjectDoesNotExist

from favoritos.models import *
from produto.models import Produto

# Create your views here.

def getFavId(request):
    favSession = request.session.session_key
    if not favSession:
        favSession = request.session.create()
    return favSession

def visualizarFavorito(request, quantidade = 0, fav_items = None):
    try:
        fav = Favoritos.objects.get(fav_id = getFavId(request))
        fav_items = FavItem.objects.filter(favorito = fav, esta_disponivel = True)
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
        favorito = Favoritos.objects.get(fav_id = getFavId(request))
    except Favoritos.DoesNotExist:
        favorito = Favoritos.objects.create(
            fav_id = getFavId(request)
        )
    favorito.save()

    try:
        fav_item = FavItem.objects.get(produto=produto, favorito=favorito)
        fav_item.save()
    except FavItem.DoesNotExist:
        fav_item = FavItem.objects.create(
            produto = produto,
            favorito=favorito,
        )
        fav_item.save()
    return redirect('favorito')

def diminuirQuantidadeProdutoFavorito(request, produto_id):
    fav = Favoritos.objects.get(car_id = getFavId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    fav_item = FavItem.objects.get(produto=produto, favorito=fav)
    if fav_item.quantidade > 1:
        fav_item.quantidade -= 1
        fav_item.save()
    else:
        fav_item.delete()
    return redirect('favorito')

def removerItemFavorito(request, produto_id):
    fav = Favoritos.objects.get(car_id = getFavId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    fav_item = FavItem.objects.get(produto=produto, favorito=fav)
    if fav_item.quantidade >= 1:
        fav_item.delete()
    return redirect('favorito')