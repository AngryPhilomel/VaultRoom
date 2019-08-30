from django.contrib import admin
from .models import Storages, Products, Stock, Done

class StoragesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('LM', 'name', 'barcode', 'department')
    list_display_links = ('LM', 'name',)
    search_fields = ('LM', 'name', 'barcode', 'department')


class StockAdmin(admin.ModelAdmin):
    list_display = ('storage', 'product', 'quantity')
    list_display_links = ('storage', 'product',)
    search_fields = ('quantity',)

class DoneAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'time')
    list_display_links = ('product', 'quantity')
    search_fields = ('quantity', 'time')

admin.site.register(Storages, StoragesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Done, DoneAdmin)

