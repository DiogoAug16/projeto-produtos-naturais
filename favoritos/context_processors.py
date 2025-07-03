from favoritos.models import *
from favoritos.views import getFavId

def contador(request):
    contador = 0
    try:
        fav = Favoritos.objects.filter(fav_id=getFavId(request)).first()
        if fav:
            fav_items = FavItem.objects.filter(favoritos=fav)
            for fav_item in fav_items:
                contador += fav_item.quantidade or 1
    except Favoritos.DoesNotExist:
        pass
    return dict(fav_contador=contador)
