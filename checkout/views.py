from django.shortcuts import render

# Create your views here.
def visualizarCheckout(request):
    context = {}
    return render(request, 'loja/checkout.html', context)