from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Stock, Storages, Products, Done, Control
from .forms import StockKorrSet, SearchForm, PriemkaForm, VidachaForm, ControlForm, CheckSearchForm



def index(request):
    stc = Stock.objects.select_related('product', 'storage').all()
    paginator = Paginator(stc, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    if request.method == 'POST':
        sf = SearchForm(request.POST)
        stc = Stock.objects.select_related('product', 'storage').all()
        storages = Storages.objects.all()
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            q = Q(barcode=keyword) | Q(LM=keyword)
            current_product = Products.objects.get(q)
            stc = Stock.objects.select_related('product','storage').filter(product=current_product.id)
            sf = SearchForm()
            context = {'stc': page.object_list, 'storages': storages, 'form': sf, 'page': page}
            return render(request, 'vaultroom/index.html', context)
        else:

            context = {'stc': page.object_list, 'storages': storages, 'form': sf, 'page': page}
            return render(request, 'vaultroom/index.html', context)
    else:
        stc = Stock.objects.select_related('product','storage').all()
        storages = Storages.objects.all()
        sf = SearchForm()
        context = {'stc': page.object_list, 'storages': storages, 'form': sf, 'page': page}
        return render(request, 'vaultroom/index.html', context)



def by_storage(request, storage_id):
    stc = Stock.objects.select_related('product').filter(storage=storage_id)
    storages = Storages.objects.all()
    current_storage = Storages.objects.get(pk=storage_id)

    paginator = Paginator(stc, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'stc': page.object_list, 'current_storage': current_storage, 'storages': storages, 'page': page}
    return render(request, 'vaultroom/by_storage.html', context)



def by_product(request, product_id):
    stc = Stock.objects.select_related('product', 'storage').filter(product=product_id)
    storages = Storages.objects.all()
    current_product = Products.objects.get(pk=product_id)

    paginator = Paginator(stc, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'stc': page.object_list, 'current_product': current_product, 'storages': storages, 'page': page}
    return render(request, 'vaultroom/by_product.html', context)



def done(request):
    done = Done.objects.select_related('product').order_by('-time')
    paginator = Paginator(done, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'done': page.object_list, 'page': page}
    return render(request, 'vaultroom/done.html', context)


def stockKorr(request, product_id):
    if request.method == 'POST':
        formset = StockKorrSet(request.POST, queryset= Stock.objects.select_related('product','storage').filter(product=product_id))
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('index'))
        else:
            context = {'formset': formset}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        formset = StockKorrSet(queryset=Stock.objects.select_related('product','storage').filter(product=product_id))
        context = {'form': formset}
        return render(request, 'vaultroom/stockorr.html', context)


def priemka(request):
    PF = formset_factory(PriemkaForm, extra=10)
    if request.method == 'POST':
        formset = PF(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    formBarcode = form.cleaned_data['barcode']
                    quantity = form.cleaned_data['quantity']
                    new = 1
                    #####
                    realStock = Stock.objects.all()
                    for i in realStock:
                        if formBarcode == i.product.barcode:
                            item = i
                            new = 0
                            break
                    if new == 0:
                        item.quantity = item.quantity + quantity
                        item.save()

                    else:
                        pr = Stock()
                        pr.storage = Storages.objects.get(name='ВМГТ')
                        pr.product = Products.objects.get(barcode=formBarcode)
                        pr.quantity = quantity
                        pr.save()
                    #####
            return redirect(reverse_lazy('index'))
        else:
            context = {'form': formset}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        formset = PF()
        context = {'form': formset}
        return render(request, 'vaultroom/stockorr.html', context)


def vidacha(request):
    PF = formset_factory(VidachaForm, extra=5)
    if request.method == 'POST':
        formset = PF(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    formBarcode = form.cleaned_data['barcode']
                    quantity = form.cleaned_data['quantity']
                    #####
                    realStock = Stock.objects.all()
                    for i in realStock:
                        if formBarcode == i.product.barcode:
                            item = i
                            break
                    item.quantity = item.quantity - quantity
                    item.save()

                    pr = Done()
                    pr.product = Products.objects.get(barcode=formBarcode)
                    pr.quantity = quantity
                    pr.save()

                    #####
            return redirect(reverse_lazy('index'))
        else:
            context = {'form': formset}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        formset = PF()
        context = {'form': formset}
        return render(request, 'vaultroom/stockorr.html', context)


def control(request):
    ctr = Control.objects.all()
    paginator = Paginator(ctr, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    if request.method == 'POST':
        cf = ControlForm(request.POST)
        ctr = Control.objects.all()
        if cf.is_valid():
            cf.save()
            ctr = Control.objects.all()
            cf = ControlForm()
            sf = CheckSearchForm()
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
        else:
            ctr = Control.objects.all()
            sf = CheckSearchForm()
            cf = ControlForm(request.POST)
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
    else:
        sf = CheckSearchForm(request.GET)
        if sf.is_valid():
            keyword = int(sf.cleaned_data['keyword'])
            ctr = Control.objects.filter(check=keyword)
            sf = CheckSearchForm()
            cf = ControlForm()
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
        else:
            ctr = Control.objects.all()
            sf = CheckSearchForm(request.GET)
            cf = ControlForm()
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf}
            return render(request, 'vaultroom/control.html', context)
