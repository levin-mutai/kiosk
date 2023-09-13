from django.shortcuts import render
from rest_framework import generics, viewsets, pagination, status
from rest_framework.response import Response
from .serializers import CreateProductSerializer,CreateOrderSerializer,OrderSerializer,ProductSerializer
from .models import Product, Order
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action


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
  
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
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
    # http_method_names = ["get", "post", "put", "delete"]
    serializer_class = CreateOrderSerializer
    pagination_class = LargePagination

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        test = OrderSerializer(serializer.data)
        return Response(
            test.data, status=status.HTTP_201_CREATED, headers=headers
        )
  
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
 
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = OrderSerializer(self.get_object())
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        self.perform_destroy(serializer)
        return Response(serializer.data)
