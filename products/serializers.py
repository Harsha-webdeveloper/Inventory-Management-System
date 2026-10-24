from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source = "category.name",
        read_only = True
    )
    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "price must be greater than 0"
            )
        return value

    def validate_quantity(self, value):
        if value < 0 :
            raise serializers.ValidationError(
                "Quantity cannot be negative"
            )
        return value

    def validate(self,attrs):
        quantity = attrs.get("quantity",0)
        minimum_stock = attrs.get("minimum_stock",0)

        if minimum_stock > quantity :
            raise serializers.ValidationError({
                "minimum_stock":(
                    "Minimum stock cannot be greater"
                    "than available quantity."
                )
            })
        return attrs

    def validate_sku(self,value):
        queryset = Product.objects.filter(sku=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A product with this SKU already exists"
            )
        return value
