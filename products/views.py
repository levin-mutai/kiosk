from django.shortcuts import render
from rest_framework import generics, viewsets, pagination, status
from rest_framework.response import Response
from .serializers import CreateOrderProductSerializer, CreateProductSerializer,CreateOrderSerializer,OrderSerializer,ProductSerializer, UpdateOrderProductSerializer
from .models import OrderProduct, Product, Order
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page

class LargePagination(pagination.PageNumberPagination):
    """Class for custom Pagination"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViews(viewsets.ModelViewSet):
    """
    Viewset to allows creation of products in the database.

    """
    serializer_class = CreateProductSerializer
    http_method_names = ["get", "post", "put", "delete"]
    pagination_class = LargePagination
    queryset = Product.objects.all()
    permission_classes = [AllowAny]



    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

 
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
    @cache_page(60 * 15, key_prefix=  'product_list') 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
 
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
 
    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)
 
    def destroy(self, request, pk=None):
        serializer = self.serializer_class(self.get_object())
        self.perform_destroy(serializer)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Allows creation, update and delete of orders
    """
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    http_method_names = ["get", "post", "put", "delete","options"]
    serializer_class = CreateOrderSerializer
    pagination_class = LargePagination

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        products = request.data.pop('products')
        user = request.data.pop('customer')

        order = Order.objects.create(customer=User.objects.get(id = user))
        for product in products:
            serialize = CreateOrderProductSerializer(data=product)
            serialize.is_valid(raise_exception=True)
            OrderProduct.objects.create(order=order, product=Product.objects.get(id=product['product']), quantity=product['quantity'])

        headers = self.get_success_headers(order.id)
        
        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id
            }, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = OrderSerializer(self.get_object())
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            order = self.get_object() 
            order.delete() 
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)
        

class OrderProductViewSet(viewsets.ModelViewSet):
    """
    Allows creation, update and delete of order products
    """
    permission_classes = [AllowAny]
    queryset = OrderProduct.objects.all()
    http_method_names = ["put", "delete","options"]
    serializer_class = CreateOrderProductSerializer
    pagination_class = LargePagination

    def get_queryset(self):
        queryset = OrderProduct.objects.all()
        return queryset

    def update(self, request,pk=None, *args, **kwargs):
        partial = True
        instance = self.get_object()
        
        serializer = UpdateOrderProductSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data) 
    def destroy(self, request, pk=None):
        try:
            order_product = self.get_object() 
            order_product.delete() 
            return Response({"message": "Order product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except OrderProduct.DoesNotExist:
            return Response("Order product not found", status=status.HTTP_404_NOT_FOUND)