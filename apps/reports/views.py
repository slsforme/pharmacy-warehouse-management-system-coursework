from datetime import date, datetime
from decimal import Decimal
import csv
import io

import openpyxl
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .dashboard import get_dashboard_data
from .generators import (
    generate_invoice_docx, generate_invoice_pdf,
    generate_sales_report_docx, generate_sales_report_pdf,
    generate_stock_report_docx, generate_stock_report_pdf,
)
from .selectors import get_arrival_for_invoice, get_sales_by_group, get_stock_by_group
from apps.inventory.models import Arrival


# ===== Вспомогательные функции =====

def _get_format(request) -> str:
    return request.query_params.get("format", "pdf").lower()


def _export_stock_csv(data: list[dict]) -> HttpResponse:
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="stock_{date.today()}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Группа", "Препарат", "Остаток"])
    for group in data:
        for drug in group["drugs"]:
            writer.writerow([group["group"], drug["name"], drug["quantity"]])
    return response


def _export_stock_excel(data: list[dict]) -> HttpResponse:
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


def _export_sales_csv(data: list[dict], date_from, date_to) -> HttpResponse:
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


def _export_sales_excel(data: list[dict], date_from, date_to) -> HttpResponse:
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


# ===== Админка: Дэшборд =====

@staff_member_required
def dashboard_view(request):
    data = get_dashboard_data()
    return render(request, "reports/dashboard.html", {
        **data,
        "title": "Дэшборд",
    })


# ===== Админка: Отчёты по остаткам =====

@staff_member_required
def stock_pdf(request):
    data = get_stock_by_group()
    buf = generate_stock_report_pdf(data)
    r = HttpResponse(buf.getvalue(), content_type="application/pdf")
    r["Content-Disposition"] = f'attachment; filename="stock_{date.today()}.pdf"'
    return r


@staff_member_required
def stock_docx(request):
    data = get_stock_by_group()
    buf = generate_stock_report_docx(data)
    r = HttpResponse(
        buf.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    r["Content-Disposition"] = f'attachment; filename="stock_{date.today()}.docx"'
    return r


@staff_member_required
def stock_csv(request):
    return _export_stock_csv(get_stock_by_group())


@staff_member_required
def stock_excel(request):
    return _export_stock_excel(get_stock_by_group())


# ===== Админка: Отчёты по продажам =====

@staff_member_required
def sales_pdf(request):
    date_from = date.today().replace(day=1)
    date_to = date.today()
    data = get_sales_by_group(date_from, date_to)
    buf = generate_sales_report_pdf(data, date_from, date_to)
    r = HttpResponse(buf.getvalue(), content_type="application/pdf")
    r["Content-Disposition"] = f'attachment; filename="sales_{date_from}_{date_to}.pdf"'
    return r


@staff_member_required
def sales_docx(request):
    date_from = date.today().replace(day=1)
    date_to = date.today()
    data = get_sales_by_group(date_from, date_to)
    buf = generate_sales_report_docx(data, date_from, date_to)
    r = HttpResponse(
        buf.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    r["Content-Disposition"] = f'attachment; filename="sales_{date_from}_{date_to}.docx"'
    return r


@staff_member_required
def sales_csv(request):
    date_from = date.today().replace(day=1)
    date_to = date.today()
    return _export_sales_csv(get_sales_by_group(date_from, date_to), date_from, date_to)


@staff_member_required
def sales_excel(request):
    date_from = date.today().replace(day=1)
    date_to = date.today()
    return _export_sales_excel(get_sales_by_group(date_from, date_to), date_from, date_to)


# ===== API: Отчёты =====
class StockReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fmt: str = "pdf"):
        data = get_stock_by_group()
        fmt = fmt.lower()

        if fmt == "docx":
            buf = generate_stock_report_docx(data)
            r = HttpResponse(
                buf.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            r["Content-Disposition"] = f'attachment; filename="stock_report_{date.today()}.docx"'
        else:
            buf = generate_stock_report_pdf(data)
            r = HttpResponse(buf.getvalue(), content_type="application/pdf")
            r["Content-Disposition"] = f'attachment; filename="stock_report_{date.today()}.pdf"'

        return r


class SalesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fmt: str = "pdf"):
        try:
            date_from = datetime.strptime(
                request.query_params.get("date_from", date.today().replace(day=1).isoformat()),
                "%Y-%m-%d",
            ).date()
            date_to = datetime.strptime(
                request.query_params.get("date_to", date.today().isoformat()),
                "%Y-%m-%d",
            ).date()
        except ValueError:
            return Response(
                {"error": "Неверный формат даты. Используйте YYYY-MM-DD"},
                status=400,
            )

        data = get_sales_by_group(date_from, date_to)
        fmt = fmt.lower()

        if fmt == "docx":
            buf = generate_sales_report_docx(data, date_from, date_to)
            r = HttpResponse(
                buf.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            r["Content-Disposition"] = f'attachment; filename="sales_report_{date_from}_{date_to}.docx"'
        else:
            buf = generate_sales_report_pdf(data, date_from, date_to)
            r = HttpResponse(buf.getvalue(), content_type="application/pdf")
            r["Content-Disposition"] = f'attachment; filename="sales_report_{date_from}_{date_to}.pdf"'

        return r


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, arrival_id: int, fmt: str = "pdf"):
        try:
            data = get_arrival_for_invoice(arrival_id)
        except Arrival.DoesNotExist:
            raise Http404("Поставка не найдена")
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        fmt = fmt.lower()

        if fmt == "docx":
            buf = generate_invoice_docx(data)
            r = HttpResponse(
                buf.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            r["Content-Disposition"] = f'attachment; filename="invoice_{data["document_number"]}.docx"'
        else:
            buf = generate_invoice_pdf(data)
            r = HttpResponse(buf.getvalue(), content_type="application/pdf")
            r["Content-Disposition"] = f'attachment; filename="invoice_{data["document_number"]}.pdf"'

        return r