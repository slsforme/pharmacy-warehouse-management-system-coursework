from .dashboard import get_dashboard_data


def dashboard_callback(request, context):
    data = get_dashboard_data()
    context.update({
        "kpi_cards": [
            {"title": "Препаратов в базе",  "metric": str(data["summary"]["total_drugs"]),        "footer": "всего в каталоге"},
            {"title": "Продаж за месяц",    "metric": str(data["summary"]["sales_this_month"]),   "footer": "за текущий месяц"},
            {"title": "Мало на складе",     "metric": str(data["summary"]["low_stock_count"]),    "footer": "менее 10 единиц"},
            {"title": "Нет на складе",      "metric": str(data["summary"]["out_of_stock"]),       "footer": "требуют пополнения"},
        ],
        "stock_by_group": data["stock_by_group"],
        "sales_last_30":  data["sales_last_30"],
        "top_drugs":      data["top_drugs"],
    })
    return context