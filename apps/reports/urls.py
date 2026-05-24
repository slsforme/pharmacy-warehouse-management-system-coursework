from django.urls import path
from .views import InvoiceView, SalesReportView, StockReportView

urlpatterns = [
    path("stock/<str:fmt>/", StockReportView.as_view(), name="report-stock"),
    path("sales/<str:fmt>/", SalesReportView.as_view(), name="report-sales"),
    path("invoice/<int:arrival_id>/<str:fmt>/", InvoiceView.as_view(), name="report-invoice"),
]