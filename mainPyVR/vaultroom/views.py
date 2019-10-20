from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Stock, Storages, Products, Done, Control, Move
from .forms import StockKorrSet, SearchForm, PriemkaForm, VidachaForm, ControlForm, CheckSearchForm, CommentForm, DateSearchForm, to_Form



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
            paginator = Paginator(stc, 30)
            if 'page' in request.GET:
                page_num = request.GET['page']
            else:
                page_num = 1
            page = paginator.get_page(page_num)
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
    done = Done.objects.select_related('product', 'storage').order_by('-time')
    storages = Storages.objects.all()
    paginator = Paginator(done, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'done': page.object_list, 'page': page, 'storages': storages}
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


def priemka(request, storage_id):
    PF = formset_factory(PriemkaForm, extra=10)
    current_storage = Storages.objects.get(pk=storage_id)
    if request.method == 'POST':
        formset = PF(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    formBarcode = form.cleaned_data['barcode']
                    quantity = form.cleaned_data['quantity']
                    new = 1
                    #####
                    realStock = Stock.objects.filter(storage=current_storage)
                    for i in realStock:
                        if formBarcode == i.product.barcode:
                            item = i
                            new = 0
                            break
                        elif formBarcode == i.product.LM:
                            item = i
                            new = 0
                            break

                    if new == 0:
                        item.quantity = item.quantity + quantity
                        item.save()

                    else:
                        pr = Stock()
                        pr.storage = current_storage
                        q = Q(barcode=formBarcode) | Q(LM=formBarcode)
                        pr.product = Products.objects.get(q)
                        pr.quantity = quantity
                        pr.save()
                    #####
            return redirect('/storage/{}'.format(storage_id))
        else:
            do = 'Добавление'
            context = {'form': formset, 'current_storage': current_storage, 'do': do}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        formset = PF()
        do = 'Добавление'
        context = {'form': formset, 'current_storage': current_storage, 'do': do}
        return render(request, 'vaultroom/stockorr.html', context)


def vidacha(request, storage_id):
    current_storage = Storages.objects.get(pk=storage_id)
    PF = formset_factory(VidachaForm, extra=5)
    if request.method == 'POST':
        formset = PF(request.POST, form_kwargs={'storage': storage_id})
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    formBarcode = form.cleaned_data['barcode']
                    quantity = form.cleaned_data['quantity']
                    #####

                    realStock = Stock.objects.select_related('product').filter(storage=current_storage)
                    for i in realStock:
                        if formBarcode == i.product.barcode:
                            item = i
                            break
                        if formBarcode == i.product.LM:
                            item = i
                            formBarcode = i.product.barcode
                            break

                    item.quantity = item.quantity - quantity
                    item.save()

                    pr = Done()
                    pr.product = Products.objects.get(barcode=formBarcode)
                    pr.storage = current_storage
                    pr.quantity = quantity
                    pr.save()

                    #####
            return redirect('/storage/{}'.format(storage_id))
        else:
            do = 'Списание'
            context = {'form': formset, 'current_storage': current_storage, 'do': do}
            return render(request, 'vaultroom/stockorr.html', context)
    else:
        do = 'Списание'
        formset = PF(form_kwargs={'storage': storage_id})
        context = {'form': formset, 'current_storage': current_storage, 'do': do}
        return render(request, 'vaultroom/stockorr.html', context)


def control(request):
    if request.method == 'POST':
        cf = ControlForm(request.POST)
        ctr = Control.objects.all()
        paginator = Paginator(ctr, 30)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        if cf.is_valid():
            cf.save()
            ctr = Control.objects.all()
            paginator = Paginator(ctr, 30)
            if 'page' in request.GET:
                page_num = request.GET['page']
            else:
                page_num = 1
            page = paginator.get_page(page_num)
            post = cf.cleaned_data['post']
            cf = ControlForm(initial={'post': post })
            cf.fields['check'].widget.attrs['autofocus'] = 'on'
            cf.fields['comment'].widget.attrs['rows'] = 3
            sf = CheckSearchForm()
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
        else:
            ctr = Control.objects.all()
            paginator = Paginator(ctr, 30)
            if 'page' in request.GET:
                page_num = request.GET['page']
            else:
                page_num = 1
            page = paginator.get_page(page_num)
            sf = CheckSearchForm()
            cf = ControlForm(request.POST)
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
    else:
        sf = CheckSearchForm(request.GET)
        if sf.is_valid():
            keyword = int(sf.cleaned_data['keyword'])
            ctr = Control.objects.filter(check=keyword)
            paginator = Paginator(ctr, 30)
            if 'page' in request.GET:
                page_num = request.GET['page']
            else:
                page_num = 1
            page = paginator.get_page(page_num)
            sf = CheckSearchForm()
            cf = ControlForm()
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)
        else:
            ctr = Control.objects.all()
            paginator = Paginator(ctr, 30)
            if 'page' in request.GET:
                page_num = request.GET['page']
            else:
                page_num = 1
            page = paginator.get_page(page_num)
            sf = CheckSearchForm(request.GET)
            cf = ControlForm()
            cf.fields['check'].widget.attrs['autofocus'] = 'on'
            cf.fields['comment'].widget.attrs['rows'] = 3
            context = {'ctr': page.object_list, 'form': cf, 'checksearchform': sf, 'page': page}
            return render(request, 'vaultroom/control.html', context)


def comment(request, check_id):
    if request.method == 'POST':
        ctr = Control.objects.get(id=check_id)
        form = CommentForm(request.POST, instance=ctr)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('control'))
        else:
            context = {'form': form}
            return render(request, 'vaultroom/comment.html', context)
    else:
        ctr = Control.objects.get(id=check_id)
        form = CommentForm(instance=ctr)
        context = {'form': form}
        return render(request, 'vaultroom/comment.html', context)

def dateDone(request):
	if request.method == 'POST':
		df = DateSearchForm(request.POST)
		day = request.POST['date_day']
		month = request.POST['date_month']
		year = request.POST['date_year']
		if df.is_valid():
			return redirect('/done/{}/{}/{}/'.format(year, month, day))
		else:
			df = DateSearchForm()
			context = {'df': df}
			return render(request, 'vaultroom/datesearch.html', context)

	else:
		df = DateSearchForm()
		context = {'df':df}
		return render(request, 'vaultroom/datesearch.html', context)


def dateControl(request):
	if request.method == 'POST':
		df = DateSearchForm(request.POST)
		day = request.POST['date_day']
		month = request.POST['date_month']
		year = request.POST['date_year']
		if df.is_valid():
			return redirect('/control/{}/{}/{}/'.format(year, month, day))
		else:
			df = DateSearchForm()
			context = {'df': df}
			return render(request, 'vaultroom/datesearch.html', context)

	else:
		df = DateSearchForm()
		context = {'df':df}
		return render(request, 'vaultroom/datesearch.html', context)

def to(request, storage_id, storage_to):
	current_storage = Storages.objects.get(id=storage_id)
	to_storage = Storages.objects.get(id=storage_to)
	storages = Storages.objects.all()
	TF = formset_factory(to_Form, extra=5)
	if request.method == 'POST':
		formset = TF(request.POST, form_kwargs={'storage': storage_id})
		if formset.is_valid():
			for form in formset:
				if form.cleaned_data:
					formBarcode = form.cleaned_data['barcode']
					quantity = form.cleaned_data['quantity']
					#####

					realStock = Stock.objects.select_related('product').filter(storage=current_storage)
					toStock = Stock.objects.select_related('product').filter(storage=to_storage)
					new = 1
					for i in realStock:
						if formBarcode == i.product.barcode:
							item = i
							break
						if formBarcode == i.product.LM:
							item = i
							formBarcode = i.product.barcode
							break

					item.quantity = item.quantity - quantity
					item.save()

						######################
					for i in toStock:
						if formBarcode == i.product.barcode:
							toitem = i
							new = 0
							break
						elif formBarcode == i.product.LM:
							toitem = i
							new = 0
							break

					if new == 0:
						toitem.quantity = toitem.quantity + quantity
						toitem.save()

					else:
						pr = Stock()
						pr.storage = to_storage
						q = Q(barcode=formBarcode) | Q(LM=formBarcode)
						pr.product = Products.objects.get(q)
						pr.quantity = quantity
						pr.save()
						######################

					mv = Move()
					mv.fromstorage = current_storage
					mv.tostorage = to_storage
					q = Q(barcode=formBarcode) | Q(LM=formBarcode)
					mv.product = Products.objects.get(q)
					mv.quantity = quantity
					mv.save()

					return redirect('/storage/{}'.format(storage_id))
		else:
			do = 'Списание'
			context = {'form': formset, 'current_storage': current_storage, 'do': do}
			return render(request, 'vaultroom/stockorr.html', context)
	else:
		do = '-> {}'.format(to_storage.name)
		formset = TF(form_kwargs={'storage': storage_id})
		context={'form': formset, 'storages': storages, 'current_storage': current_storage, 'do': do}
		return render(request, 'vaultroom/stockorr.html', context)


def move(request):
	move = Move.objects.select_related('product', 'tostorage', 'fromstorage').order_by('-time')
	storages = Storages.objects.all()
	paginator = Paginator(move, 30)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'move': page.object_list, 'page': page, 'storages': storages}
	return render(request, 'vaultroom/move.html', context)


def dateMove(request):
	if request.method == 'POST':
		df = DateSearchForm(request.POST)
		day = request.POST['date_day']
		month = request.POST['date_month']
		year = request.POST['date_year']
		if df.is_valid():
			return redirect('/move/{}/{}/{}/'.format(year, month, day))
		else:
			df = DateSearchForm()
			context = {'df': df}
			return render(request, 'vaultroom/datesearch.html', context)

	else:
		df = DateSearchForm()
		context = {'df':df}
		return render(request, 'vaultroom/datesearch.html', context)