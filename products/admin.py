from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","created_at")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "name",
                    "category",
                    "sku",
                    "cost_price",
                    "selling_price",
                    "quantity",
                    "is_active")
    search_fields=("name","sku")
    list_filter = ("category","is_active")
