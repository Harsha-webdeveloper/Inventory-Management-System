from rest_framework import serializers
from .models import Purchase,PurchaseItem
from django.db import transaction
from products.models import Product

class PurchaseItemSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source = "product.name",
        read_only = True
    )
    class Meta:
        model = PurchaseItem
        fields = ("id",
                  "product",
                  "product_name",
                  "quantity",
                  "unit_price"
                  )
        
class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializers(many=True)
    class Meta:
        model = Purchase
        fields = (
            "id" ,
            "supplier",
            "invoice_number",
            "purchase_date",
            "remarks",
            "items",
        )

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        purchase = Purchase.objects.create(**validated_data)

        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            PurchaseItem.objects.create(
                purchase = purchase,
                **item
            )
            product.quantity += quantity
            product.save()

        return purchase