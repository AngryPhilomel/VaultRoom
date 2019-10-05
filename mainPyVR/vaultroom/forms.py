from django.forms import modelformset_factory
from django import forms

from .models import Stock, Storages, Products

StockKorrSet = modelformset_factory(Stock, fields=('storage', 'product', 'quantity'),
								   can_delete=True, extra=0)

class PriemkaForm(forms.Form):
	barcode = forms.CharField(label='Штрихкод')
	quantity = forms.IntegerField(label='Количество')

class SearchForm(forms.Form):
	keyword = forms.CharField(label='Штрихкод')