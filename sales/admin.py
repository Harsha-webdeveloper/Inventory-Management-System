from django.contrib import admin
from .models import Sale,SaleItem

# Register your models here.
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "customer",
        "sale_date",
    )

    inlines = [SaleItemInline]
