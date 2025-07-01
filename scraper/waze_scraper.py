import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from almacenamiento.mongo_almacenamiento import insertar_eventos, contar_eventos_db

# Configuración
MAX_EVENTOS = 10000
PAUSA_SEGUNDOS = 20  # Tiempo de espera entre capturas

async def interceptar_eventos(page):
    """Intercepta las respuestas de Waze Live Map."""
    last_data = None

    async def handle_response(response):
        if '/api/georss' in response.url:
            try:
                json_data = await response.json()
                nonlocal last_data
                last_data = json_data
            except Exception as e:
                print(f"Error al procesar JSON: {e}")

    page.on("response", handle_response)
    await asyncio.sleep(10)  # Espera para asegurar la captura
    return last_data

async def preparar_mapa(page):
    """Cierra posibles pop-ups y ajusta el zoom del mapa."""
    try:
        await page.click(".waze-tour-tooltip__acknowledge", timeout=5000)
    except:
        pass
    try:
        for _ in range(3):
            await page.click(".leaflet-control-zoom-out")
            await asyncio.sleep(1)
    except:
        pass

async def capturar_eventos(playwright):
    """Captura eventos del mapa de Waze."""
    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ]
    )
    context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    page = await context.new_page()

    await page.goto(
        "https://www.waze.com/es-419/live-map/",
        wait_until="domcontentloaded", 
        timeout=120000  # 2 minutos máximo de espera
    )

    await preparar_mapa(page)
    data = await interceptar_eventos(page)
    await browser.close()

    if data:
        guardar_eventos(data)
    else:
        print(f"[{datetime.now()}] No se obtuvieron datos esta vez.")

def guardar_eventos(data):
    """Guarda los eventos capturados en MongoDB."""
    eventos = []
    for jam in data.get("jams", []):
        eventos.append({"type": "jam", **jam})
    for alert in data.get("alerts", []):
        eventos.append({"type": "alert", **alert})

    if eventos:
        insertar_eventos(eventos)  # Guardamos en MongoDB
        print(f"[{datetime.now()}] {len(eventos)} eventos guardados en MongoDB.")
    else:
        print(f"[{datetime.now()}] No se encontraron eventos para guardar.")

def iniciar_scraper():
    """Función principal para iniciar el proceso de scraping y almacenamiento."""
    async def ejecutar():
        total_eventos = contar_eventos_db()
        print(f"Eventos actuales en MongoDB: {total_eventos}/{MAX_EVENTOS}")

        async with async_playwright() as playwright:
            while total_eventos < MAX_EVENTOS:
                await capturar_eventos(playwright)
                total_eventos = contar_eventos_db()
                print(f"Total acumulado en MongoDB: {total_eventos}/{MAX_EVENTOS}")

                if total_eventos < MAX_EVENTOS:
                    print(f"Esperando {PAUSA_SEGUNDOS} segundos antes de la siguiente captura...")
                    await asyncio.sleep(PAUSA_SEGUNDOS)

        print("10.000 eventos capturados en MongoDB.")

    asyncio.run(ejecutar())