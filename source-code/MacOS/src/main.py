import subprocess, os, time, sys, re, shutil
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAVE_EXE_PATH = os.path.abspath(os.path.join(BASE_DIR, "Brave-Browser", "Contents", "MacOS", "Brave Browser"))
FFMPEG_PATH = "ffmpeg"
VIDEO_DIR = os.path.join(os.path.expanduser("~"), "Movies", "ArtlistVideos")
os.makedirs(VIDEO_DIR, exist_ok=True)

SUPPORTED_RESOLUTIONS = {
    '2160': ["4k", "3840x2160", "2160p", "uhd"],
    '1080': ["hd", "1080p", "fhd", "1920x1080"],
    '720': ["720p", "1280x720"],
    '480': ["480p", "640x480", "sd"],
    '240': ["240p", "426x240"]
}
DEFAULT_RESOLUTION = '1080'

def convert(m3u8_url, sel_res, logger=print):
    latest_file = os.path.join(VIDEO_DIR, "latest.mp4")
    if os.path.exists(latest_file):
        count = 1
        while os.path.exists(os.path.join(VIDEO_DIR, f"output_{count}.mp4")):
            count += 1
        os.rename(latest_file, os.path.join(VIDEO_DIR, f"output_{count}.mp4"))

    if not shutil.which(FFMPEG_PATH):
        logger(f'FFMPEG NOT FOUND AT: {FFMPEG_PATH}')
        return
    
    # note! 240p=0, 360p=1, 480p=2, 720p=3, 1080p=4, 2160p=5
    res_to_idx = {
        '240': '0',
        '360': '1',
        '480': '2',
        '720': '3',
        '1080': '4',
        '2160': '5'
    }
    idx = res_to_idx.get(sel_res, '4')

    command = [
        FFMPEG_PATH, "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", m3u8_url,
        "-map", f"0:p:{idx}", 
        "-c", "copy", 
        "-bsf:a", "aac_adtstoasc", 
        latest_file
    ]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            if "size=" in line:
                sys.stdout.write(f"\rProcess: {line.strip()}")
                sys.stdout.flush()
            else:
                logger(line.strip())

        process.wait()
        logger(f'\nSuccessfully created {latest_file} at {sel_res}p!')

    except Exception as e:
        logger(f"FFMPEG failed: {e}")

def click_render_play_button(page):
    target_btn = page.locator("button[data-testid='renderButton']").filter(has_text="Play").first
    if target_btn.is_visible():
        target_btn.scroll_into_view_if_needed()
        target_btn.click(force=True)
        return True
    return False

def get_m3u8_link(target_url):
    if not os.path.exists(BRAVE_EXE_PATH):
        print(f"BRAVE NOT FOUND AT: {BRAVE_EXE_PATH}")
        return None

    m3u8_link = None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=BRAVE_EXE_PATH, headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def handle_request(request):
            nonlocal m3u8_link
            if ".m3u8" in request.url.lower() and not m3u8_link:
                m3u8_link = request.url

        page.on("request", handle_request)

        try:
            print("Extracting raw video...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2)
            page.mouse.wheel(0, 500)

            for _ in range(5):
                if m3u8_link: break
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Browser Error: {e}")

        browser.close()
        return m3u8_link

def fix_resolution(m3u8_url, sel_res):
    if not m3u8_url: return None
    pattern = r"(_)\d+p(?=[._])"
    replacement = f"\\g<1>{sel_res}p"
    return re.sub(pattern, replacement, m3u8_url)

def finalize(resolution, url, logger=print):
    link = get_m3u8_link(url)
    if link:
        patched = fix_resolution(link, resolution)
        convert(patched, resolution, logger=logger)
        return True
    else:
        logger("Failed to find any m3u8 link.")
        return False

def debug_mode():
    while True:
        url = input("\nEnter a URL: ").strip()
        if not url: continue
        link = get_m3u8_link(url)
        if link:
            print('file extracted!')
        else:
            print("Failed to find link.")

if __name__ == "__main__":
    # debug_mode()
    pass