from rest_framework import viewsets,filters
from .models import Category, Product
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ProductPermission

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [ProductPermission]

    queryset = Product.objects.select_related("category").all().order_by("id")
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    #search products by name,sku,description
    search_fields = [
        "name",
        "sku",
        "description"
    ]
    #filter products by category & is_active 
    filterset_fields = [
        "category",
        "is_active",
    ]
    # order by price,quantity & name by asc & desc
    ordering_fields = [
        "price",
        "quantity",
        "name",
    ]
    # default ordering by name 
    ordering = [
        "name"
    ]