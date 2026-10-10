# Временные логотипы-заглушки: круг с буквой «Х». Заменить, когда будет настоящий логотип.
import sys
from PIL import Image, ImageDraw, ImageFont
root = sys.argv[1] + "/frontend/static/images/"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def mark(size, fg=(0, 0, 0, 255), bg=(0, 0, 0, 0)):
    s = size * 4
    im = Image.new("RGBA", (s, s), bg)
    d = ImageDraw.Draw(im)
    w = max(4, s // 14)
    d.ellipse([w, w, s - w, s - w], outline=fg, width=w)
    f = ImageFont.truetype(BOLD, int(s * 0.56))
    d.text((s / 2, s / 2), "Х", font=f, fill=fg, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)

for n in (128, 256, 512, 1024):
    mark(n).save(root + f"logo/logo-{n}.png")
mark(256, fg=(255, 255, 255, 255)).save(root + "logo/logo-white-256.png")

wt = Image.new("RGBA", (900, 256), (0, 0, 0, 0))
wt.alpha_composite(mark(256, fg=(255, 255, 255, 255)))
ImageDraw.Draw(wt).text((290, 128), "Хезеллих", font=ImageFont.truetype(BOLD, 110), fill="white", anchor="lm")
wt.save(root + "logo/logo-white-text.png")

white = (255, 255, 255, 255)
for name, n in [("android-chrome-192x192", 192), ("android-chrome-512x512", 512), ("apple-touch-icon", 180),
                ("favicon-16x16", 16), ("favicon-32x32", 32)]:
    im = Image.new("RGBA", (n, n), white); im.alpha_composite(mark(n)); im.save(root + f"favicon/{name}.png")
ico = Image.new("RGBA", (48, 48), white); ico.alpha_composite(mark(48))
ico.save(root + "favicon/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

share = Image.new("RGBA", (1200, 630), white)
share.alpha_composite(mark(300), (450, 110))
ImageDraw.Draw(share).text((600, 500), "Хезеллих", font=ImageFont.truetype(BOLD, 72), fill="black", anchor="mm")
share.convert("RGB").save(root + "share.png")
share.save(root + "the_machine_logo.png")

ava = Image.new("RGB", (192, 192), (200, 200, 200))
d = ImageDraw.Draw(ava)
d.ellipse([66, 36, 126, 96], fill=(245, 245, 245)); d.ellipse([36, 106, 156, 226], fill=(245, 245, 245))
ava.save(root + "avatar.png")

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><style>@media (prefers-color-scheme:dark){{*{{stroke:{c}}}text{{fill:{c}}}}}</style><circle cx="256" cy="256" r="230" fill="none" stroke="#000" stroke-width="36"/><text x="256" y="256" font-family="DejaVu Sans,Arial,sans-serif" font-weight="700" font-size="290" text-anchor="middle" dominant-baseline="central" fill="#000">Х</text></svg>'''
open(root + "favicon/favicon.svg", "w").write(svg.format(c="#000"))
open(root + "favicon/favicon-dark.svg", "w").write(svg.format(c="#fff").replace('#000"', '#fff"'))
print("ok")

# фон для лендинга (тёмная тема): светлый знак, приглушённый, чтобы не спорить с заголовком
hero = mark(1024, fg=(255, 255, 255, 40))
hero.save(root + "logo/logo-hero.png")
print("hero ok")
