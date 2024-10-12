from django.shortcuts import render
from django.http import HttpResponse


def show_item(request, item_id):
    return render(request, 'app/item.html', {'item_id: item_id'})


def home(request):
    return render(request, 'catalog/home.html')


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Ваше сообщение "{message}" получено.')
    return render(request, 'catalog/contacts.html')