# ArtlistIO Video Downloader

**Author:** Mu_rpy  
**Platform:** Windows & MacOS (currently)

ArtlistIO is a simple tool to extract and convert `.m3u8` streams from websites to MP4 using FFmpeg and Playwright.  

> [!CAUTION]
> If you dont want to be held responsible for pirating stock footage, buy an artlist.io license at [their plans and pricing page](https://artlist.io/page/pricing/max).
> You are adviced to  [terms of service](https://artlist.io/help-center/privacy-terms/terms-of-use/) and understand how you are violating them.

> [!WARNING]
> This is for educational purposes only.
> By continuing to use this, you accept the risks and acknowledge that you have been warned.

> [!NOTE]
> This is not theft! The m3u8 files are sent to the user's browser via network payload, this script simply reconstructs said file into mp4s. Even when the user didnt accept the terms and agreements. Suck it.

---

## Features

- Works for most stock footage websites
- Choose resolution (2160p / 1080p / 720p / 480p)  
- Automatically saves videos into the user's `videos/` folder  
- Opens the folder automatically when conversion finishes  
- Minimal, responsive, yellow-themed UI 

## Installation & Usage

### Windows
Go to the [Releases](https://github.com/da036b97b7c705909d6ffbd2e3349128/ArtlistIO-video-downloader/releases) page and download the latest Windows installer (.exe) or ZIP.

**Using Setup.exe (Recommended)**
1. If using the latest version. run the setup file.
The setup will:
    - Verify Python installation.
    - Install dependencies via Pipenv.
    - Launch the local web server and open your browser to http://127.0.0.1:8000.
    - Enter the Artlist URL, select your resolution, and click Convert. The video will appear in your Videos/ArtlistVideos folder automatically.

**Using start.bat (Experimental)**
1. If using the ZIP, run start.bat.
2. If it crashes you're gonna have to do `pip install playwright` then rerun the start.bat again. (The piplock file doesnt have playwright in it)


### macOS

1. Download the latest macOS ZIP from the [Releases](https://github.com/da036b97b7c705909d6ffbd2e3349128/ArtlistIO-video-downloader/releases) page.

2. Extract the folder and open a Terminal in that directory.

3. Run the following command to give the script permission to run: `chmod +x start.command`

4. Double-click start.command.

5. The script will:
    - Display the License agreement (type yes to continue).
    - Check for Homebrew and Python (will install them automatically if missing).
    - Install all dependencies and launch the server.

6. Access the UI at http://127.0.0.1:8000.

### Linux systems
Still working on a script for linux users, but for now you can follow the same format as the macOS zip.
Just replace the chromium & ffmpeg folders with ones that support your distro. Then chmod x+ the start.sh

## Notes:
- Currently only tested on Windows, should also work in macOS.
- Do not commit large video files; the repo tracks videos/ in .gitignore.
- The website will be active unil you shutdown manually (via website button), end task it, or shutdown/reboot your device.

---

Mu_rpy © 2026
