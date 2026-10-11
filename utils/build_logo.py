"""
Собирает все файлы логотипа из исходников в frontend/static/images/logo/src/:
PNG разных размеров, фавиконки, картинку для соцсетей и фон для лендинга.

    uv run --with playwright python utils/build_logo.py   # нужен установленный chromium для playwright

Исходники: logo-light.svg / logo-dark.svg (знак + название), mark.svg (знак с паром), icon.svg (знак без пара).
"""
import io
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "static", "images")
SRC = os.path.join(ROOT, "logo", "src")


def render(page, svg_name, width, height, background="transparent"):
    svg = open(os.path.join(SRC, svg_name)).read()
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(
        f'<html><body style="margin:0;background:{background};display:flex;align-items:center;'
        f'justify-content:center;width:{width}px;height:{height}px">'
        f'<div style="width:{width}px;height:{height}px;display:flex;align-items:center;justify-content:center">'
        f'{svg.replace("<svg ", "<svg style=\'max-width:100%;max-height:100%;width:100%;height:100%\' ", 1)}'
        f'</div></body></html>'
    )
    png = page.screenshot(omit_background=(background == "transparent"))
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # знак для шапки сайта и аватарок
        for size in (128, 256, 512, 1024):
            render(page, "icon.svg", size, size).save(os.path.join(ROOT, "logo", f"logo-{size}.png"))

        # полный логотип
        render(page, "logo-light.svg", 1200, 210).save(os.path.join(ROOT, "logo", "logo-full.png"))
        render(page, "logo-dark.svg", 1200, 210).save(os.path.join(ROOT, "logo", "logo-white-text.png"))

        # фон лендинга: крупный приглушённый знак
        hero = render(page, "mark.svg", 1024, 1024)
        alpha = hero.getchannel("A").point(lambda a: int(a * 0.07))
        hero.putalpha(alpha)
        hero.save(os.path.join(ROOT, "logo", "logo-hero.png"))

        # фавиконки (на белом, чтобы были видны на тёмных вкладках)
        fav = os.path.join(ROOT, "favicon")
        for name, size in [("android-chrome-192x192", 192), ("android-chrome-512x512", 512),
                           ("apple-touch-icon", 180), ("favicon-16x16", 16), ("favicon-32x32", 32)]:
            render(page, "icon.svg", size, size, background="#FFFFFF").save(os.path.join(fav, f"{name}.png"))
        ico = render(page, "icon.svg", 48, 48, background="#FFFFFF")
        ico.save(os.path.join(fav, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
        icon_svg = open(os.path.join(SRC, "icon.svg")).read()
        open(os.path.join(fav, "favicon.svg"), "w").write(icon_svg)

        # превью для соцсетей 1200x630
        share = render(page, "logo-light.svg", 1000, 630, background="#FFFFFF")
        canvas = Image.new("RGBA", (1200, 630), "#FFFFFF")
        canvas.alpha_composite(share, (100, 0))
        canvas.convert("RGB").save(os.path.join(ROOT, "share.png"))
        canvas.convert("RGB").save(os.path.join(ROOT, "the_machine_logo.png"))

        browser.close()
    print("ok")


if __name__ == "__main__":
    sys.exit(main())
