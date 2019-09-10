from django.forms import modelformset_factory

from .models import Stock, Storages, Products

StockKorrSet = modelformset_factory(Stock, fields=('storage', 'product', 'quantity'),
								   can_delete=True, extra=0)
