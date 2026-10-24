from django.contrib import admin
from .models import Purchase,PurchaseItem
# Register your models here.

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1 

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display=(
        "invoice_number",
        "supplier",
        "purchase_date",
    )

    inlines = [
        PurchaseItemInline,
    ]