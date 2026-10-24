from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from .models import Sale,SaleItem
from products.models import Product

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source = "product.name",
        read_only = True
    )
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = SaleItem
        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "line_total"
        )
        read_only_fields = (
            "unit_price",
            "line_total"
        )

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many = True)
    class Meta:
        model = Sale
        fields = (
            "id",
            "customer",
            "invoice_number",
            "sale_date",
            "remarks",
            "items",
        )

    read_only_fields=(
        "sub_total",
        "discount",
        "tax",
        "grand_total",
    )

    def validate(self,attrs):
        items = attrs.get("items",[])
        if not items:
            raise serializers.ValidationError(
                "At least one sale item is required"
            )
        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            if quantity <= 0:
                raise serializers.ValidationError(
                    {
                        "quantity":
                        f"Quantity must be greater than zero for {product.name}"
                    }
                )
            if quantity > product.quantity:
                raise serializers.ValidationError(
                    {
                        "stock":
                        f"Insufficient stock for {product.name}"
                    }
                )
        return attrs
    
    @transaction.atomic
    def create(self,validated_data):
        items = validated_data.pop("items")
        sub_total = Decimal("0.00")

        for item in items:
            quantity = item["quantity"]
            product = item["product"]
            sub_total += quantity * product.selling_price

        discount = Decimal("0.00")
        tax = sub_total * Decimal("0.18") # 18% GST
        print(type(sub_total), sub_total)
        print(type(discount), discount)
        print(type(tax), tax)
        
        grand_total = sub_total - discount + tax

        #create Sale
        sale = Sale.objects.create(
            sub_total = sub_total,
            discount = discount,
            tax = tax,
            grand_total =grand_total,
            **validated_data
        )

# create sale item & reduce stock 

        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            SaleItem.objects.create(
                sale=sale,
                product = product,
                quantity = quantity,
                unit_price = product.selling_price,
            )

            Product.objects.filter(
                pk = product.pk
            ).update(
                quantity = F("quantity") - quantity
            )
        return sale




