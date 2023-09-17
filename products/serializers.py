from rest_framework import serializers
from .models import Order, Product,OrderProduct,Customer


#===========================================Product Serializer ========================================


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
class GetProductSerializer(ProductSerializer):
    class Meta:
        model = ProductSerializer.Meta.model
        exclude = ['created_at', 'updated_at']

#==========================================Ordered Product Serializer ========================================

class OrderProductSerializer(serializers.ModelSerializer):
    product = GetProductSerializer()
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

#==========================================Order Serializer ========================================     
    
class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name="get_products")

    

    class Meta:
        model = Order
        fields = ('id', 'customer',"total_price","created_at", "updated_at", 'products')

    def get_products(self, obj):
        orderProd = OrderProduct.objects.filter(order_id=obj.id)
        serialized_data = OrderProductSerializer(orderProd, many=True)
        
        return serialized_data.data
    

class CreateOrderSerializer(serializers.ModelSerializer):
    products = CreateOrderProductSerializer(many=True)
    
    
    class Meta:
        model = Order
        fields = ( 'customer', 'products',)

    def create(self, validated_data):
        products_datas = validated_data.pop('products')
        print(products_datas)
        order = Order.objects.create(**validated_data)

        for product_data in products_datas:
            quantity = product_data['quantity']
            OrderProduct.objects.create(order=order, product=product_data['product'], quantity=quantity)

        return order
   

   #=============================================Customer Serializer==========================================

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CreateCustomerSerilaizer(CustomerSerializer):
    class Meta:
        model = CustomerSerializer.Meta.model
        exclude = ['created_at', 'updated_at',"id"]

class UpdateCustomerSerializer(CreateCustomerSerilaizer):
    class Meta:
        model = CreateCustomerSerilaizer.Meta.model
        exclude = ['user']