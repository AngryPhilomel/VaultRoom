from django.forms import modelformset_factory
from django import forms
from django.core.exceptions import ValidationError

from .models import Stock, Storages, Products

StockKorrSet = modelformset_factory(Stock, fields=('storage', 'product', 'quantity'),
								   can_delete=True, extra=0)

class PriemkaForm(forms.Form):
	barcode = forms.IntegerField(label='Штрихкод')
	quantity = forms.IntegerField(label='Количество')

	def clean_barcode(self):
		ok=0
		barcode = int(self.cleaned_data['barcode'])
		valid = Products.objects.all()
		for i in valid:
			if barcode == i.barcode:
				ok = 1
				break
		if ok != 1:
			raise ValidationError('Товар не найден')

	def clean_quantity(self):
		quantity = int(self.cleaned_data['quantity'])
		if quantity < 1:
			raise ValidationError('Введите корректное количество')




class SearchForm(forms.Form):
	keyword = forms.CharField(label='Штрихкод')