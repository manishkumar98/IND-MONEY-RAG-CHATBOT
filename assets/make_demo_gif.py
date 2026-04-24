"""
Generates assets/demo.gif by driving the frontend with Playwright.
Intercepts HTTPS requests to the Render backend and proxies them to
a locally running FastAPI server (localhost:8000).
"""
import io
import json
import requests
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_HTML = PROJECT_ROOT / "frontend" / "index.html"
OUT_GIF = PROJECT_ROOT / "assets" / "demo.gif"

QUESTIONS = [
    "What is the 3 year return of SBI Flexicap Fund?",
    "What is the risk level of SBI Small Cap Fund?",
    "Should I invest in SBI Midcap Fund?",
]

frames: list[Image.Image] = []
durations: list[int] = []


def snap(page, ms: int = 80):
    png = page.screenshot()
    img = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = img.size
    img = img.resize((w // 2, h // 2), Image.LANCZOS)
    frames.append(img)
    durations.append(ms)


def hold(page, ms: int = 1200):
    snap(page, ms)


def proxy_to_local(route):
    local_url = route.request.url.replace(
        "https://sbi-mf-backend.onrender.com", "http://localhost:8000"
    )
    try:
        resp = requests.request(
            method=route.request.method,
            url=local_url,
            headers={k: v for k, v in route.request.headers.items()
                     if k.lower() not in ("host", "origin", "referer")},
            data=route.request.post_data,
            timeout=30,
        )
        route.fulfill(
            status=resp.status_code,
            headers=dict(resp.headers),
            body=resp.content,
        )
    except Exception as e:
        route.fulfill(status=500, body=json.dumps({"answer": f"proxy error: {e}"}))


def run_demo(page):
    page.route("https://sbi-mf-backend.onrender.com/**", proxy_to_local)
    page.goto(FRONTEND_HTML.as_uri())
    page.wait_for_load_state("networkidle")
    hold(page, 1500)

    for question in QUESTIONS:
        inp = page.locator("#user-input")
        inp.click()
        for ch in question:
            inp.type(ch, delay=0)
            snap(page, 35)

        hold(page, 600)
        page.locator("#send-btn").click()

        page.wait_for_selector(".chat-bubble.loading", state="detached", timeout=30000)
        hold(page, 2500)

        inp.fill("")
        page.wait_for_timeout(150)

    hold(page, 3000)


with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    run_demo(page)
    browser.close()

OUT_GIF.parent.mkdir(exist_ok=True)
frames[0].save(
    OUT_GIF,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=False,
)
print(f"✅ Saved {OUT_GIF}  ({len(frames)} frames, {OUT_GIF.stat().st_size // 1024} KB)")
