from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from catalog.models import Product


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Ваше сообщение "{message}" получено.')
    return render(request, 'contacts.html')
