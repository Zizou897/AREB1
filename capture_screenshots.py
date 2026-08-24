"""Capture les screenshots des sites existants pour les cards projets.

Usage : python capture_screenshots.py
Sorties : static/img/projects/*.png + *.webp (1200px max, qualité 85)
"""

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path(__file__).parent / "static" / "img" / "projects"

SITES = [
    ("ctams", "https://www.ctams.net"),
    ("monappligestion_online", "https://monapplidegestion.online"),
    ("monappligestion_net", "https://monapplidegestion.net"),
]

DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
TIMEOUT_MS = 30_000
MAX_WIDTH = 1200
WEBP_QUALITY = 85


def optimize(png_bytes: bytes, dest_png: Path) -> None:
    """Redimensionne à 1200px max, sauvegarde PNG + WebP."""
    img = Image.open(BytesIO(png_bytes))
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        img = img.resize((MAX_WIDTH, round(img.height * ratio)), Image.LANCZOS)
    img.save(dest_png, "PNG", optimize=True)
    img.save(dest_png.with_suffix(".webp"), "WEBP", quality=WEBP_QUALITY)
    print(f"  -> {dest_png.name} ({img.width}x{img.height}) + .webp")


def goto_with_retry(page, url: str) -> bool:
    for attempt in (1, 2):
        try:
            page.goto(url, wait_until="networkidle", timeout=TIMEOUT_MS)
            return True
        except PlaywrightTimeout:
            print(f"  timeout (essai {attempt}/2) sur {url}")
        except Exception as exc:  # site down, DNS, SSL...
            print(f"  erreur (essai {attempt}/2) sur {url} : {exc}")
    return False


def capture_site(browser, slug: str, url: str) -> bool:
    print(f"\n[{slug}] {url}")
    ok = False

    # Desktop : pleine page + hero (viewport)
    ctx = browser.new_context(viewport=DESKTOP, device_scale_factor=2)
    page = ctx.new_page()
    if goto_with_retry(page, url):
        page.wait_for_timeout(2000)  # laisser finir les animations d'entrée
        optimize(page.screenshot(full_page=True), OUTPUT_DIR / f"{slug}_desktop_full.png")
        optimize(page.screenshot(), OUTPUT_DIR / f"{slug}_desktop.png")
        ok = True
    ctx.close()

    # Mobile : viewport uniquement
    ctx = browser.new_context(viewport=MOBILE, device_scale_factor=2, is_mobile=True)
    page = ctx.new_page()
    if goto_with_retry(page, url):
        page.wait_for_timeout(2000)
        optimize(page.screenshot(), OUTPUT_DIR / f"{slug}_mobile.png")
        ok = True
    ctx.close()

    return ok


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for slug, url in SITES:
            results[slug] = capture_site(browser, slug, url)
        browser.close()

    print("\n--- Bilan ---")
    for slug, ok in results.items():
        print(f"  {slug}: {'OK' if ok else 'ECHEC'}")
    return 0 if any(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
