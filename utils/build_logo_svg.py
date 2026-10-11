"""Исходники логотипа «Хезеллих» (SVG): uv run --with fonttools --with brotli python utils/build_logo_svg.py <путь к nunito-cyrillic-900-normal.woff2 из @fontsource/nunito> frontend/static/images/logo/src
Текст переводится в контуры (шрифт Nunito Black, лицензия SIL OFL), чтобы SVG не зависел от шрифтов."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]
OUT = sys.argv[2]

TERRACOTTA = "#B85C3E"
MUSTARD = "#E2A93B"
TEAL = "#0E6E66"
TEAL_ON_DARK = "#2FA89B"
PLUM = "#5A1A3A"
PLUM_ON_DARK = "#D98BB0"
OLIVE = "#6E7B3A"

WORD = "Хезеллих"
LETTER_COLORS = [TERRACOTTA, MUSTARD, TEAL, PLUM, OLIVE, TERRACOTTA, MUSTARD, TEAL]


def mark_paths(fg_heart="#FFFFFF", steam_on=True):
    """Знак в квадрате 0..100: чашка, низ которой переходит в хвостик облачка речи, внутри сердце, сверху пар"""
    cup = (
        # верхний край, правый бок, дно, хвостик облачка внизу слева, левый бок
        "M12 40 H74 C74 60 68 74 54 79 L26 79 L16 91 L18 77 C14 72 12 58 12 40 Z"
    )
    handle = "M73 46 C90 44 92 66 71 67 L71 60 C83 60 82 51 73 53 Z"
    heart = ("M43 70 C30 61 28 55 30 50 C32 45 39 44 43 50 "
             "C47 44 54 45 56 50 C58 55 56 61 43 70 Z")
    steam = [
        "M34 33 C29 27 39 23 34 15",
        "M48 33 C43 27 53 23 48 15",
    ]
    out = [f'<path d="{cup}" fill="{TERRACOTTA}"/>',
           f'<path d="{handle}" fill="{TERRACOTTA}"/>',
           f'<path d="{heart}" fill="{fg_heart}"/>']
    out += [] if not steam_on else [f'<path d="{s}" fill="none" stroke="{TERRACOTTA}" stroke-width="4.5" stroke-linecap="round"/>' for s in steam]
    return "\n".join(out)


def word_paths(dark=False, size=100.0):
    font = TTFont(FONT)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    scale = size / upm
    x = 0.0
    parts = []
    for ch, color in zip(WORD, LETTER_COLORS):
        if dark and color == PLUM:
            color = PLUM_ON_DARK
        if dark and color == TEAL:
            color = TEAL_ON_DARK
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set)
        # y вниз: отражаем, базовая линия на y=0
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x, 0))
        glyph_set[name].draw(tpen)
        parts.append(f'<path d="{pen.getCommands()}" fill="{color}"/>')
        x += glyph_set[name].width * scale - size * 0.01
    return "\n".join(parts), x


def svg(view_w, view_h, body, bg=None):
    rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w:.1f} {view_h:.1f}" '
            f'width="{view_w:.0f}" height="{view_h:.0f}">{rect}{body}</svg>\n')


def full_logo(dark):
    word, word_w = word_paths(dark=dark, size=100)
    # знак 100x100 масштабируем до высоты ~1.25 строчных; слово ставим на базовую линию y=88
    mark = f'<g transform="translate(-6,-7) scale(1.12)">{mark_paths()}</g>'
    word_g = f'<g transform="translate(106,82)">{word}</g>'
    return svg(106 + word_w + 4, 104, mark + word_g)


open(f"{OUT}/mark.svg", "w").write(svg(100, 100, mark_paths()))
# для фавиконки и аватарок: без пара, чашка на весь квадрат
icon = svg(88, 88, f'<g transform="translate(-6,-21)">{mark_paths(steam_on=False)}</g>')
open(f"{OUT}/icon.svg", "w").write(icon)
open(f"{OUT}/logo-light.svg", "w").write(full_logo(dark=False))
open(f"{OUT}/logo-dark.svg", "w").write(full_logo(dark=True))
print("ok")
