from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import threading, asyncio, os, sys, subprocess, webbrowser, uvicorn, signal
from main import finalize
from threading import Timer


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = FastAPI()
static_abs_path = resource_path("static")
app.mount("/static", StaticFiles(directory=static_abs_path), name="static")


def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

@app.get("/", response_class=HTMLResponse)
def index():
    index_path = os.path.join(static_abs_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


class Logger:
    def __init__(self, ws, loop):
        self.ws = ws
        self.loop = loop

    def start(self):
        asyncio.run_coroutine_threadsafe(self.ws.send_text("Conversion started..."), self.loop)

    def success(self):
        asyncio.run_coroutine_threadsafe(self.ws.send_text("Conversion successful!"), self.loop)
        folder = os.path.join(os.path.expanduser("~"), "Videos", "ArtlistVideos")
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
    resolution = int(data["resolution"])
    loop = asyncio.get_running_loop()
    logger = Logger(ws, loop)

    def run_finalize():
        def ws_logger(message):
            asyncio.run_coroutine_threadsafe(ws.send_text(message), loop)

        ws_logger("Searching for video stream...")
        try:
            if finalize(resolution, url): logger.success()
            else: logger.fail()
            
        except Exception as e:
            ws_logger(f"Error: {str(e)}")
            logger.fail()

    threading.Thread(target=run_finalize, daemon=True).start()

@app.get("/shutdown")
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return "Server shutting down..."

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None, ws="websockets")