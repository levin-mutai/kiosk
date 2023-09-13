from rest_framework import serializers
from .models import Order, Product,OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "stock",
            "description",
            "image_url",
        )
class GetOrderProductSerializer(ProductSerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        exclude = ['created_at', 'updated_at']

class OrderProductSerializer(serializers.ModelSerializer):
    # product = GetOrderProductSerializer()
    class Meta:
        model = OrderProduct
        fields = ( 'quantity',"product", "total_price")

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'products',"created_at", "updated_at",)


class CreateOrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ( 'user_id', 'products',)
   