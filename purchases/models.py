from django.db import models
from suppliers.models import Supplier
from products.models import Product

# Create your models here.

class Purchase(models.Model):
    supplier = models.ForeignKey(
       Supplier,
       on_delete=models.PROTECT,
       related_name="purchases", 
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True,
    )

    purchase_date = models.DateField()
    remarks = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    def __str__(self):
        return self.invoice_number

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    def __str__(self):
        return self.product.name
    