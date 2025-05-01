import matplotlib
matplotlib.use("Agg")  # 🔒 Используем безопасный бэкэнд без GUI

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from analysis_core import run_volatility_analysis
from generate_report import generate_pdf_report, get_plot_data

app = FastAPI()

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(zip=zip)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    print("🔍 Загружается шаблон index.html")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, days: int = Form(...)):
    crypto_results, sp500_result = run_volatility_analysis(days)
    generate_pdf_report()
    plot_data = get_plot_data()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "days": days,
        "crypto_results": crypto_results,
        "sp500_result": sp500_result,
        "report_url": "/download/report",
        "plot_data": plot_data,
        "crypto_tables": [coin["daily_data"] for coin in crypto_results],
        "sp500_table": sp500_result["daily_data"]
    })

@app.get("/download/report")
def download_report():
    filepath = "crypto_volatility_report.pdf"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type='application/pdf', filename="volatility_report.pdf")
    return {"error": "Файл не найден"}
