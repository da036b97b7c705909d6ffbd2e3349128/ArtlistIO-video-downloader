from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import threading, asyncio, os
from main import finalize

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


class Logger:
    def __init__(self, ws, loop):
        self.ws = ws
        self.loop = loop

    def start(self):
        asyncio.run_coroutine_threadsafe(self.ws.send_text("Conversion started..."), self.loop)

    def success(self):
        asyncio.run_coroutine_threadsafe(self.ws.send_text("Conversion successful!"), self.loop)
        folder = os.path.join(os.path.dirname(__file__), "videos")
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.startfile(folder)

    def fail(self):
        asyncio.run_coroutine_threadsafe(self.ws.send_text("Conversion failed!"), self.loop)


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    data = await ws.receive_json()
    url = data["url"]
    resolution = data["resolution"]
    loop = asyncio.get_running_loop()
    logger = Logger(ws, loop)

    def run_finalize():
        logger.start()
        try:
            finalize(resolution, url, logger=print)
            logger.success()
        except:
            logger.fail()

    threading.Thread(target=run_finalize, daemon=True).start()
