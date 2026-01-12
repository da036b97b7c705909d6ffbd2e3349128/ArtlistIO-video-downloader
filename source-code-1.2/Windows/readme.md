## Artlist.IO Video Downloader (Windows Source)
This folder contains the source code and build configurations for the Windows version of the Artlist.IO Video Downloader.

## Installation & Setup
Ensure you have Python and Pipenv installed on your system.
1. Install Dependencies: Open your terminal in this directory and run: 
```bash
pipenv install
```

2. Activate Environment: 
```bash
pipenv shell
```
or 

```bash
pipenv run
```

3. Run from Source:
```bash
python src/app.py
```

## 🏗 Building the Application
If you want to compile the standalone .exe file, use the following PyInstaller command:
```bash
pipenv run pyinstaller --noconfirm --onefile --windowed --add-data "src/static;static" --add-data "src/ffmpeg;ffmpeg" --add-data "src/chromium;chromium" --hidden-import="websockets" --hidden-import="uvicorn.logging" src/app.py
```

> ![NOTE]
> The included .iss file is for the legacy 1.1 version of this repository. 
> It was used for creating a setup.exe installer and is not required for 
> the current version's portable application workflow.

🚀 HOW TO USE!!!
1. Open the application: Run the compiled .exe or start via Python.
2. Access the Dashboard: Open your browser and navigate to: http://127.0.0.1:8000
3. Download: Enter a URL, choose your resolution, and click Convert.
4. Find your files: Converted videos are saved automatically to: %USERPROFILE%\Videos\ArtlistVideos

> [!WARNING] The local server will continue to run until you:
> Stop it via the shutdown button on the website.
> End the process via Task Manager.
> Shutdown or reboot your computer.

Have fun! :>

---
Mu_rpy © 2026
