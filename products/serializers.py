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
    product = GetOrderProductSerializer()
    class Meta:
        model = OrderProduct
        fields = ("id","product", "quantity","total_price")

class CreateOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ("product", "quantity","total_price")
class UpdateOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ("product", "quantity")
        
    
class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name="get_products")

    

    class Meta:
        model = Order
        fields = ('id', 'user_id',"total_price","created_at", "updated_at", 'products')

    def get_products(self, obj):
        orderProd = OrderProduct.objects.filter(order_id=obj.id)
        serialized_data = OrderProductSerializer(orderProd, many=True)
        
        return serialized_data.data
    

class CreateOrderSerializer(serializers.ModelSerializer):
    products = CreateOrderProductSerializer(many=True)
    
    
    class Meta:
        model = Order
        fields = ( 'user_id', 'products',)

    def create(self, validated_data):
        products_datas = validated_data.pop('products')
        print(products_datas)
        order = Order.objects.create(**validated_data)

        for product_data in products_datas:
            quantity = product_data['quantity']
            OrderProduct.objects.create(order=order, product=product_data['product'], quantity=quantity)

        return order
   