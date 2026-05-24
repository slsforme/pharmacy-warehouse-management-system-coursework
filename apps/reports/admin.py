import csv
import io
from datetime import date

import openpyxl
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from unfold.admin import ModelAdmin

from .dashboard import get_dashboard_data
from .generators import (
    generate_sales_report_docx, generate_sales_report_pdf,
    generate_stock_report_docx, generate_stock_report_pdf,
)
from .selectors import get_sales_by_group, get_stock_by_group


def export_stock_csv(data: list[dict]) -> HttpResponse:
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="stock_{date.today()}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Группа", "Препарат", "Остаток"])
    for group in data:
        for drug in group["drugs"]:
            writer.writerow([group["group"], drug["name"], drug["quantity"]])
    return response


def export_stock_excel(data: list[dict]) -> HttpResponse:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Остатки"
    ws.append(["Группа", "Препарат", "Остаток"])
    for group in data:
        for drug in group["drugs"]:
            ws.append([group["group"], drug["name"], drug["quantity"]])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="stock_{date.today()}.xlsx"'
    return response


def export_sales_csv(data: list[dict], date_from, date_to) -> HttpResponse:
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="sales_{date_from}_{date_to}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Группа", "Препарат", "Количество", "Сумма"])
    for group in data:
        for drug in group["drugs"]:
            writer.writerow([
                group["group"],
                drug["drug__name"],
                drug["quantity"],
                drug["amount"],
            ])
    return response


def export_sales_excel(data: list[dict], date_from, date_to) -> HttpResponse:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Продажи"
    ws.append(["Группа", "Препарат", "Количество", "Сумма"])
    for group in data:
        for drug in group["drugs"]:
            ws.append([
                group["group"],
                drug["drug__name"],
                drug["quantity"],
                float(drug["amount"]),
            ])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="sales_{date_from}_{date_to}.xlsx"'
    return response


class ReportsAdminSite(ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            # Отчёты PDF/DOCX
            path("stock/pdf/",  self.admin_site.admin_view(self.stock_pdf),  name="report_stock_pdf"),
            path("stock/docx/", self.admin_site.admin_view(self.stock_docx), name="report_stock_docx"),
            path("sales/pdf/",  self.admin_site.admin_view(self.sales_pdf),  name="report_sales_pdf"),
            path("sales/docx/", self.admin_site.admin_view(self.sales_docx), name="report_sales_docx"),
            # Экспорт CSV/Excel
            path("stock/csv/",   self.admin_site.admin_view(self.stock_csv),   name="report_stock_csv"),
            path("stock/excel/", self.admin_site.admin_view(self.stock_excel), name="report_stock_excel"),
            path("sales/csv/",   self.admin_site.admin_view(self.sales_csv),   name="report_sales_csv"),
            path("sales/excel/", self.admin_site.admin_view(self.sales_excel), name="report_sales_excel"),
        ]
        return custom + urls

    def stock_pdf(self, request):
        buf = generate_stock_report_pdf(get_stock_by_group())
        r = HttpResponse(buf.getvalue(), content_type="application/pdf")
        r["Content-Disposition"] = "attachment; filename=stock_report.pdf"
        return r

    def stock_docx(self, request):
        buf = generate_stock_report_docx(get_stock_by_group())
        r = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        r["Content-Disposition"] = "attachment; filename=stock_report.docx"
        return r

    def sales_pdf(self, request):
        date_from = date.today().replace(day=1)
        date_to = date.today()
        buf = generate_sales_report_pdf(get_sales_by_group(date_from, date_to), date_from, date_to)
        r = HttpResponse(buf.getvalue(), content_type="application/pdf")
        r["Content-Disposition"] = "attachment; filename=sales_report.pdf"
        return r

    def sales_docx(self, request):
        date_from = date.today().replace(day=1)
        date_to = date.today()
        buf = generate_sales_report_docx(get_sales_by_group(date_from, date_to), date_from, date_to)
        r = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        r["Content-Disposition"] = "attachment; filename=sales_report.docx"
        return r

    def stock_csv(self, request):
        return export_stock_csv(get_stock_by_group())

    def stock_excel(self, request):
        return export_stock_excel(get_stock_by_group())

    def sales_csv(self, request):
        date_from = date.today().replace(day=1)
        date_to = date.today()
        return export_sales_csv(get_sales_by_group(date_from, date_to), date_from, date_to)

    def sales_excel(self, request):
        date_from = date.today().replace(day=1)
        date_to = date.today()
        return export_sales_excel(get_sales_by_group(date_from, date_to), date_from, date_to)