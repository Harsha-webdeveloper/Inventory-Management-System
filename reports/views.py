from decimal import Decimal
from django.db.models import Sum,F,ExpressionWrapper,DecimalField
from django.db.models.functions import ExtractMonth
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product
from customers.models import Customer
from suppliers.models import Supplier
from purchases.models import Purchase,PurchaseItem
from sales.models import Sale,SaleItem
from products.serializers import ProductSerializer

class DashboardAPIView(APIView):
    def get(self,request):
        data = {
            "total_products": Product.objects.count(),
            "total_customers":Customer.objects.count(),
            "total_suppliers":Supplier.objects.count(),

            "total_sales":
                Sale.objects.aggregate(
                    total = Sum("grand_total")
                )["total"] or Decimal("0.00"),

            "total_purchases" :Purchase.objects.count(),

            "low_stock_products": Product.objects.filter(
                quantity__lt=10
            ).count(),
            
        }
        return Response(data)

class LowStockAPIView(APIView):
    def get(self,request):
        products = Product.objects.filter(
            quantity__lt =10
        )
        serializer = ProductSerializer(
            products,
            many=True
        )
        return Response(serializer.data)

class MonthlySalesAPIView(APIView):
    def get(seld, request):
        monthly_sales = ( Sale.objects.annotate
                         (month = ExtractMonth("sale_date"))
                         .values("month")
                         .annotate(total_sales=Sum("grand_total"))
                         .order_by("month")
        )

        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        data = []
        for item in monthly_sales:
            data.append({
                "month":month_names[item["month"]],
                "total_sales":item["total_sales"],
            })
        return Response(data)

class MonthlyPurchaseAPIView(APIView):
    def get(self,request):
        monthly_purchases = (
            PurchaseItem.objects
            .annotate(
                total_amount = ExpressionWrapper(
                    F("quantity") * F("unit_price"),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2,                        
                    )
                )
            ).annotate(
                month = ExtractMonth("purchase__purchase_date")
            )
            .values("month")
            .annotate(
                total_purchase=Sum("total_amount")
            )
            .order_by("month")
        )
        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        data = []
        for item in monthly_purchases:
            data.append({
                "month":month_names[item["month"]],
                "total_purchase": item["total_purchase"],
            })

        return Response(data)

class TopSellingProductAPIView(APIView):
    def get(self,request):
        top_products = (SaleItem.objects
        .values(
            "product",
            "product__name"
        )
        .annotate(sold_quantity = Sum("quantity"))
        .order_by("-sold_quantity")
        )

        data = []
        for item in top_products:
            data.append({
                "product":item["product__name"],
                "quantity"  : item["sold_quantity"],
            })
        return Response(data)

class ProfitReportAPIView(APIView):
    def get(self,request):
        profitreport = (SaleItem.objects.values(
            "product",
            "product__name"
        ).annotate(
            total_quantity = Sum("quantity"),
            total_profit = Sum(
                ExpressionWrapper(
                    F("quantity") *
                    (
                        F("unit_price") - F("product__cost_price")
                    ),
                    output_field = DecimalField(max_digits=15,decimal_places=2) 
                )
            )
        ).order_by("-total_profit")
        )

        data = []
        for item in profitreport:
            data.append({
                "product" : item["product__name"],
                "total_quantity" : item["total_quantity"],
                "total_profit": item["total_profit"]
            })

        return Response(data)

class SalesDateRangeAPIView(APIView):
    def get(self,request):
        start_date = request.query_params.get("start_date"),
        end_date = request.query_params.get("end date")

        if not start_date or not end_date:
            return Response(
                {
                    "error":"start date & end date is required"
                },
                status = 400
                )   
        sales = Sale.objects.filter(
            sale_date__range = [start_date,end_date]
        ).order_by("sale_date")

        data = []
        for sale in sales:
            data.append({
                "invoice_number" : sale.invoice_number,
                "customer" : sale.customer.name,
                "sale_date" : sale.sale_date,
                "grand_total":sale.grand_total
            })

        return Response(data)