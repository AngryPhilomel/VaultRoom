from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Stock, Storages, Products, Done
from .forms import StockKorrSet



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


def stockKorr(request, product_id):
    if request.method == 'POST':
        formset = StockKorrSet(request.POST, queryset= Stock.objects.filter(product=product_id))
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('index'))
        else:
            context = {'formset': formset}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        formset = StockKorrSet(queryset=Stock.objects.filter(product=product_id))
        context = {'form': formset}
        return render(request, 'vaultroom/stockorr.html', context)


