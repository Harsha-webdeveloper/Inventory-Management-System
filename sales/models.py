from django.db import models
from customers.models import Customer
from products.models import Product
# Create your models here.

class Sale(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    invoice_number = models.CharField(max_length=100,unique=True)
    sale_date = models.DateField()
    remarks = models.TextField(blank=True)
    sub_total = models.DecimalField(max_digits=12,
                                    decimal_places=2,default=0)
    
    discount = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    tax = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    grand_total = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
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

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.product.name