from rest_framework import serializers
from .models import Storages, Stock, Products

class StoragesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Storages
		fields = ('id','name')

class ProductsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Products
		fields = ('id', 'LM', 'barcode', 'name', 'department')

class StockSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	storage_id = serializers.IntegerField()#write_only=True)
	storage = StoragesSerializer(read_only=True)
	product_id = serializers.IntegerField()#write_only=True)
	product = ProductsSerializer(read_only=True)
	quantity = serializers.IntegerField()
	class Meta:
		model = Stock
		fields = ('id','storage_id','storage', 'product_id','product', 'quantity')


