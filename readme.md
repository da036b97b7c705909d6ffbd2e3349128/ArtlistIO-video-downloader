# ArtlistIO Stock Footage

**Author:** Mu_rpy  
**Platform:** Windows only (currently)

ArtlistIO is a simple tool to extract and convert `.m3u8` streams from websites to MP4 using FFmpeg and Playwright.  

---

## Features

- Convert `.m3u8` or page URLs into MP4  
- Choose resolution (2160p / 1080p / 720p / 480p)  
- Automatically saves videos into a `videos/` folder  
- Opens the folder automatically when conversion finishes  
- Minimal, responsive, yellow-themed UI  

---

## Requirements

- Windows 10/11  
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

2. Open start.bat (automated setup & run).

The batch file will:

    - Check if Python is installed

    - If not, run your Python installer from python_redist/ folder

    - Install Pipenv and project dependencies

    - Install Playwright browsers

    - Start the FastAPI server

3. Open your browser and go to:

```cpp
http://127.0.0.1:8000
```

4. Enter a URL and choose resolution, then click Convert. The converted video will appear in the videos/ folder automatically.

Notes:
- Currently only tested on Windows.

- Do not commit large video files; the repo tracks videos/ in .gitignore.

---

Mu_rpy © 2026