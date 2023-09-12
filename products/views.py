from django.shortcuts import render
from rest_framework import generics, viewsets, pagination, status
from rest_framework.response import Response
from serializers import CreateProductsSerializer
from models import Product


# Create your views here.


class LargePAgination(pagination.PageNumberPagination):
    """Class for custom Pagination"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViews(generics.CreateAPIView):
    serializer_class = CreateProductsSerializer
    pagination_class = LargePAgination
    queryset = Product.objects.all()

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

    queryset = Product.objects.all()
    serializer_class = CreateProductsSerializer
    pagination_class = LargePAgination

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
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        self.perform_destroy(serializer)
        return Response(serializer.data)
