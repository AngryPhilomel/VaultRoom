from django.shortcuts import render
from django.http import HttpResponse

from .models import Stock, Storages, Products, Done

def index(request):
    stc = Stock.objects.all()
    storages = Storages.objects.all()
    context = {'stc': stc, 'storages': storages}
    return render(request, 'vaultroom/index.html', context)

def by_storage(request, storage_id):
    stc = Stock.objects.filter(storage=storage_id)
    storages = Storages.objects.all()
    current_storage = Storages.objects.get(pk=storage_id)
    context = {'stc': stc, 'current_storage': current_storage, 'storages': storages,}
    return render(request, 'vaultroom/by_storage.html', context)

def by_product(request, product_id):
    stc = Stock.objects.filter(product=product_id)
    storages = Storages.objects.all()
    current_product = Products.objects.get(pk=product_id)
    context = {'stc': stc, 'current_product': current_product, 'storages': storages,}
    return render(request, 'vaultroom/by_product.html', context)

def done(request):
    done = Done.objects.order_by('-time')
    context = {'done': done}
    return render(request, 'vaultroom/done.html', context)

