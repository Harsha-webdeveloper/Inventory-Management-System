from django.contrib import admin
from .models import Supplier
# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display=(
        "company_name",
        "name",
        "email",
        "phone",
        "is_active"
    )

    search_fields=(
        "company_name",
        "name",
    )