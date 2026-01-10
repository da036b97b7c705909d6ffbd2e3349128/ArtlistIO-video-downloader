# ArtlistIO Stock Footage

**Author:** Mu_rpy  
**Platform:** Windows & MacOS (currently)

ArtlistIO is a simple tool to extract and convert `.m3u8` streams from websites to MP4 using FFmpeg and Playwright.  

> [!CAUTION]
> If you dont want to be held responsible for pirating stock footage, buy an artlist.io license at [their plans and pricing page](https://artlist.io/page/pricing/max).
> You are adviced to  [terms of service](https://artlist.io/help-center/privacy-terms/terms-of-use/) and understand how you are violating them.

> [!WARNING]
> This is for educational purposes only.
> By continuing to use this, you accept the risks and acknowledge that you have been warned.

---

## Features

- Works for most trademarked websites
- Choose resolution (2160p / 1080p / 720p / 480p)  
- Automatically saves videos into a `videos/` folder  
- Opens the folder automatically when conversion finishes  
- Minimal, responsive, yellow-themed UI  

---

## Requirements

- Python 3.10+  
- Pipenv  

All Python dependencies are tracked in `Pipfile`:

```text
fastapi
uvicorn
playwright
```

## Installation & Usage


1. Go to the [Releases](https://github.com/da036b97b7c705909d6ffbd2e3349128/ArtlistIO-stock-footage-extractor/releases) page and download the latest release ZIP.

2. Open start.bat or start.sh (automated setup & run).

The batch or SH file will:

    - Check if Python is installed

    - If not, run your Python installer from redist/ folder

    - Install Pipenv and project dependencies

    - Install Playwright browsers

    - Start the FastAPI server

3. Open your browser and go to:

```cpp
http://127.0.0.1:8000
```

4. Enter a URL and choose resolution (default is 4K), then click Convert. The converted video will appear in the videos/ folder automatically.

Notes:
- Currently only tested on Windows, should also work in macOS.

- Do not commit large video files; the repo tracks videos/ in .gitignore.

---

Mu_rpy © 2026
