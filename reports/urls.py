from django.urls import path
from .views import DashboardAPIView,LowStockAPIView,MonthlySalesAPIView,MonthlyPurchaseAPIView,TopSellingProductAPIView,ProfitReportAPIView

urlpatterns = [
    path(
        "reports/dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard"
    ),
    path(
        "reports/low-stock/",
        LowStockAPIView.as_view()
    ),
    path(
        "reports/monthly-sales/",
        MonthlySalesAPIView.as_view(),
    ),
    path(
        "reports/monthly-purchase",
        MonthlyPurchaseAPIView.as_view(),
    ),
    path(
        "reports/top-selling-products",
        TopSellingProductAPIView.as_view(),
    ),
    path(
        "reports/profit",
        ProfitReportAPIView.as_view()
    )
]