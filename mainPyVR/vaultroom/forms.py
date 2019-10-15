from django.forms import modelformset_factory, modelform_factory
from django import forms
from django.core.exceptions import ValidationError

from .models import Stock, Storages, Products, Control

StockKorrSet = modelformset_factory(Stock, fields=('storage', 'product', 'quantity'),
								   can_delete=True, extra=0)

class PriemkaForm(forms.Form):
	barcode = forms.IntegerField(label='Штрихкод\LM')
	quantity = forms.IntegerField(label='Количество')

	def clean_barcode(self):
		ok=0
		barcode = int(self.cleaned_data['barcode'])
		valid = Products.objects.all()
		for i in valid:
			if barcode == i.barcode:
				ok = 1
				break
			if barcode == i.LM:
				ok = 1
				break
		if ok != 1:
			raise ValidationError('Товар не найден')
		return barcode

	def clean_quantity(self):
		quantity = int(self.cleaned_data['quantity'])
		if quantity < 1:
			raise ValidationError('Введите корректное количество')
		return quantity


class VidachaForm(forms.Form):
	barcode = forms.IntegerField(label='Штрихкод\LM')
	quantity = forms.IntegerField(label='Количество')

	def clean_barcode(self):
		ok=0
		barcode = int(self.cleaned_data['barcode'])
		valid = Stock.objects.select_related('product').all()
		for i in valid:
			if barcode == i.product.barcode:
				ok = 1
				break
			if barcode == i.product.LM:
				ok = 1
				break
		if ok != 1:
			raise ValidationError('Товар не найден')
		return barcode

	def clean_quantity(self):
		quantity = int(self.cleaned_data['quantity'])
		try:
			barcode = int(self.cleaned_data['barcode'])
		except:
			raise ValidationError('Товар не найден')
		valid = Stock.objects.select_related('product').all()

		for i in valid:
			if barcode == i.product.barcode:
				current_quantity = i.quantity
				break
			if barcode == i.product.LM:
				current_quantity = i.quantity
				break

		if quantity < 1:
			raise ValidationError('Введите корректное количество')
		if quantity > current_quantity:
			raise ValidationError('Недостаточно товара')
		return quantity


class SearchForm(forms.Form):
	keyword = forms.IntegerField(label='Штрихкод\LM')

	def clean_keyword(self):
		ok=0
		keyword = self.cleaned_data['keyword']
		valid = Products.objects.all()
		for i in valid:
			if keyword == i.barcode:
				ok = 1
				break
			elif keyword == i.LM:
				ok = 1
				break
		if ok != 1:
			raise ValidationError('Товар не найден')
		return keyword

ControlForm = modelform_factory(Control, fields=('check', 'post', 'comment', 'pallet'))

class CheckSearchForm(forms.Form):
	keyword = forms.IntegerField(label='Номер чека')

	def clean_keyword(self):
		ok=0
		keyword = self.cleaned_data['keyword']
		valid = Control.objects.all()
		for i in valid:
			if keyword == i.check:
				ok = 1
				break
		if ok != 1:
			raise ValidationError('Чек не найден')
		return keyword

CommentForm = modelform_factory(Control, fields=('check', 'post', 'comment', 'pallet'))


class DateSearchForm(forms.Form):
	date = forms.DateField(widget=forms.SelectDateWidget())