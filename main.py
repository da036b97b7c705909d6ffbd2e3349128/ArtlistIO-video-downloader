import subprocess, os, time, re
from playwright.sync_api import sync_playwright

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin", "ffmpeg.exe")
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

SUPPORTED_RESOLUTIONS = {
    '2160': ["4k", "3840x2160", "2160p", "uhd"],
    '1080': ["hd", "1080p", "fhd", "1920x1080"],
    '720': ["720p", "1280x720"],
    '480': ["480p", "640x480", "sd"],
    '240': ["240p", "426x240"]
}
DEFAULT_RESOLUTION = '1080'


def convert(m3u8_url, logger=print):
    latest_file = os.path.join(VIDEO_DIR, "latest.mp4")
    if os.path.exists(latest_file):
        count = 1
        while os.path.exists(os.path.join(VIDEO_DIR, f"output_{count}.mp4")):
            count += 1
        os.rename(latest_file, os.path.join(VIDEO_DIR, f"output_{count}.mp4"))

    if not os.path.exists(FFMPEG_PATH):
        logger(f'FFMPEG NOT FOUND AT: {FFMPEG_PATH}')
        return

    command = [
        FFMPEG_PATH, "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", m3u8_url, "-c", "copy", "-bsf:a", "aac_adtstoasc", latest_file
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
            logger(line.strip())

        process.wait()
        logger(f'Successfully created {latest_file}!')

    except subprocess.CalledProcessError:
        logger("FFMPEG failed!")


def get_m3u8_link(target_url):
    m3u8_link = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def handle_request(request):
            nonlocal m3u8_link
            if ".m3u8" in request.url and not m3u8_link:
                m3u8_link = request.url

        page.on("request", handle_request)

        try:
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)
            page.mouse.wheel(0, 500)
            for _ in range(20):
                if m3u8_link: break
                time.sleep(0.5)
        except Exception:
            pass

        if m3u8_link:
            logger = print
            logger("Raw file extracted!")

        browser.close()
        return m3u8_link


def fix_resolution(m3u8_url, sel_res):
    if not m3u8_url: return None
    pattern = r"_\d+p_"
    replacement = f"_{sel_res}p_"
    return re.sub(pattern, replacement, m3u8_url)



def finalize(resolution, url, logger=print):
    link = get_m3u8_link(url)
    if link:
        patched = fix_resolution(link, resolution)
        convert(patched, logger=logger)
    else:
        logger("Failed to find any m3u8 link.")


def config():
    while True:
        usr_res = input("Enter resolution [default: HD]: ").lower().strip()
        url = input("Enter a URL: ").strip()
        if not url: continue

        selected = None
        if not usr_res:
            selected = DEFAULT_RESOLUTION
        else:
            for val, matches in SUPPORTED_RESOLUTIONS.items():
                if usr_res in matches or usr_res == val:
                    selected = val
                    break

        if selected:
            finalize(selected, url)
        else:
            print(f"Invalid resolution! Using default: [{DEFAULT_RESOLUTION}p]")
            finalize(DEFAULT_RESOLUTION, url)


if __name__ == "__main__":
    config()
