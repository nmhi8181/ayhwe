from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
OUT_DIR = BASE / "figures"
OUT_DIR.mkdir(exist_ok=True)

PNG_OUT = OUT_DIR / "kerangka_teori.png"
SVG_OUT = OUT_DIR / "kerangka_teori.svg"

WIDTH = 1920
HEIGHT = 1080

COLORS = {
    "bg": "#F8F6F1",
    "navy": "#104D64",
    "teal": "#1F7A8C",
    "gold": "#D9A441",
    "green": "#5A9466",
    "ink": "#1F2933",
    "muted": "#5D6C7A",
    "line": "#D5DDE3",
    "white": "#FFFFFF",
}


def load_font(size: int, bold: bool = False):
    candidates = (
        [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf"]
        if bold
        else [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf"]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


TITLE_FONT = load_font(44, True)
SUB_FONT = load_font(24, False)
HEAD_FONT = load_font(28, True)
BODY_FONT = load_font(22, False)
SMALL_FONT = load_font(20, False)


def rounded(draw, box, fill, outline, radius=28, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, box, text, font, fill, spacing=8):
    x1, y1, x2, y2 = box
    lines = text.split("\n")
    bboxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    heights = [b[3] - b[1] for b in bboxes]
    widths = [b[2] - b[0] for b in bboxes]
    total = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + (y2 - y1 - total) / 2
    for line, w, h in zip(lines, widths, heights):
        x = x1 + (x2 - x1 - w) / 2
        draw.text((x, y), line, font=font, fill=fill)
        y += h + spacing


def left_text(draw, box, lines, font, fill, spacing=12):
    x1, y1, x2, y2 = box
    y = y1
    for line in lines:
        text = f"• {line}"
        bbox = draw.textbbox((0, 0), text, font=font)
        h = bbox[3] - bbox[1]
        draw.text((x1, y), text, font=font, fill=fill)
        y += h + spacing
        if y > y2:
            break


def arrow(draw, start, end, fill, width=8, head=24):
    draw.line([start, end], fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    if ex >= sx:
        points = [(ex, ey), (ex - head, ey - head / 2), (ex - head, ey + head / 2)]
    else:
        points = [(ex, ey), (ex + head, ey - head / 2), (ex + head, ey + head / 2)]
    draw.polygon(points, fill=fill)


def build_png():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, 120), fill=COLORS["navy"])
    draw.text((80, 30), "Kerangka Teori Kajian", font=TITLE_FONT, fill=COLORS["white"])
    draw.text(
        (82, 84),
        "Landasan teori yang menyokong hubungan faktor linguistik dan keberkesanan strategi pengajaran literasi Bahasa Melayu murid Tahap 1",
        font=SUB_FONT,
        fill="#D8E5EA",
    )

    theory_boxes = [
        ((120, 210, 560, 540), COLORS["teal"], "Teori Literasi Awal", ["Kesedaran fonologi", "Kosa kata", "Bahasa lisan", "Pengalaman awal bahasa"]),
        ((740, 210, 1180, 540), COLORS["gold"], "Simple View of Reading", ["Dekoding", "Kefahaman linguistik", "Menyokong kefahaman bacaan"]),
        ((1360, 210, 1800, 540), COLORS["green"], "Konstruktivisme Sosial Vygotsky", ["Perancah pembelajaran", "Penyesuaian strategi", "Bimbingan mengikut tahap murid"]),
    ]

    for box, accent, title, bullets in theory_boxes:
        rounded(draw, box, COLORS["white"], COLORS["line"], radius=30)
        x1, y1, x2, y2 = box
        rounded(draw, (x1, y1, x2, y1 + 72), accent, accent, radius=30, width=1)
        center_text(draw, (x1 + 10, y1 + 8, x2 - 10, y1 + 66), title, HEAD_FONT, COLORS["white"])
        left_text(draw, (x1 + 34, y1 + 110, x2 - 30, y2 - 24), bullets, BODY_FONT, COLORS["ink"], spacing=18)

    center_box = (460, 660, 1460, 860)
    rounded(draw, center_box, "#FFFDF8", COLORS["line"], radius=34)
    center_text(
        draw,
        (500, 705, 1420, 815),
        "Kerangka teori kajian\n\nFaktor linguistik murid perlu difahami melalui literasi awal dan kefahaman linguistik,\nmanakala keberkesanan strategi pengajaran dijelaskan melalui prinsip perancah dan penyesuaian pengajaran.",
        BODY_FONT,
        COLORS["ink"],
        spacing=12,
    )

    bottom_box = (640, 915, 1280, 1015)
    rounded(draw, bottom_box, COLORS["navy"], COLORS["navy"], radius=26, width=1)
    center_text(
        draw,
        bottom_box,
        "Implikasi: faktor linguistik murid mempunyai hubungan dengan\nkeberkesanan strategi pengajaran literasi Bahasa Melayu",
        HEAD_FONT,
        COLORS["white"],
        spacing=8,
    )

    for start_x in (340, 960, 1580):
        arrow(draw, (start_x, 540), (960, 660), COLORS["navy"], width=7, head=22)
    arrow(draw, (960, 860), (960, 915), COLORS["gold"], width=8, head=24)

    draw.text(
        (120, 1035),
        "Kerangka teori ini menggabungkan Teori Literasi Awal, Simple View of Reading, dan Konstruktivisme Sosial Vygotsky sebagai asas konsep kajian.",
        font=SMALL_FONT,
        fill=COLORS["muted"],
    )

    img.save(PNG_OUT, dpi=(300, 300))


def build_svg():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS['bg']}"/>
<rect x="0" y="0" width="{WIDTH}" height="120" fill="{COLORS['navy']}"/>
<text x="80" y="62" font-family="Arial, Segoe UI, sans-serif" font-size="44" font-weight="700" fill="{COLORS['white']}">Kerangka Teori Kajian</text>
<text x="82" y="96" font-family="Arial, Segoe UI, sans-serif" font-size="24" fill="#D8E5EA">Landasan teori yang menyokong hubungan faktor linguistik dan keberkesanan strategi pengajaran literasi Bahasa Melayu murid Tahap 1</text>

<rect x="120" y="210" width="440" height="330" rx="30" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="120" y="210" width="440" height="72" rx="30" fill="{COLORS['teal']}"/>
<text x="340" y="255" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="28" font-weight="700" fill="{COLORS['white']}">Teori Literasi Awal</text>
<text x="154" y="340" font-family="Arial, Segoe UI, sans-serif" font-size="22" fill="{COLORS['ink']}"><tspan x="154" dy="0">• Kesedaran fonologi</tspan><tspan x="154" dy="1.5em">• Kosa kata</tspan><tspan x="154" dy="1.5em">• Bahasa lisan</tspan><tspan x="154" dy="1.5em">• Pengalaman awal bahasa</tspan></text>

<rect x="740" y="210" width="440" height="330" rx="30" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="740" y="210" width="440" height="72" rx="30" fill="{COLORS['gold']}"/>
<text x="960" y="255" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="28" font-weight="700" fill="{COLORS['white']}">Simple View of Reading</text>
<text x="774" y="340" font-family="Arial, Segoe UI, sans-serif" font-size="22" fill="{COLORS['ink']}"><tspan x="774" dy="0">• Dekoding</tspan><tspan x="774" dy="1.5em">• Kefahaman linguistik</tspan><tspan x="774" dy="1.5em">• Menyokong kefahaman bacaan</tspan></text>

<rect x="1360" y="210" width="440" height="330" rx="30" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="1360" y="210" width="440" height="72" rx="30" fill="{COLORS['green']}"/>
<text x="1580" y="255" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="28" font-weight="700" fill="{COLORS['white']}">Konstruktivisme Sosial Vygotsky</text>
<text x="1394" y="340" font-family="Arial, Segoe UI, sans-serif" font-size="22" fill="{COLORS['ink']}"><tspan x="1394" dy="0">• Perancah pembelajaran</tspan><tspan x="1394" dy="1.5em">• Penyesuaian strategi</tspan><tspan x="1394" dy="1.5em">• Bimbingan mengikut tahap murid</tspan></text>

<rect x="460" y="660" width="1000" height="200" rx="34" fill="#FFFDF8" stroke="{COLORS['line']}" stroke-width="3"/>
<text x="960" y="735" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="22" fill="{COLORS['ink']}">
  <tspan x="960" dy="0">Kerangka teori kajian</tspan>
  <tspan x="960" dy="1.6em">Faktor linguistik murid perlu difahami melalui literasi awal dan kefahaman linguistik,</tspan>
  <tspan x="960" dy="1.4em">manakala keberkesanan strategi pengajaran dijelaskan melalui prinsip perancah dan penyesuaian pengajaran.</tspan>
</text>

<rect x="640" y="915" width="640" height="100" rx="26" fill="{COLORS['navy']}"/>
<text x="960" y="960" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="28" font-weight="700" fill="{COLORS['white']}">
  <tspan x="960" dy="0">Implikasi: faktor linguistik murid mempunyai hubungan dengan</tspan>
  <tspan x="960" dy="1.3em">keberkesanan strategi pengajaran literasi Bahasa Melayu</tspan>
</text>

<line x1="340" y1="540" x2="960" y2="660" stroke="{COLORS['navy']}" stroke-width="7"/><polygon points="960,660 938,649 938,671" fill="{COLORS['navy']}"/>
<line x1="960" y1="540" x2="960" y2="660" stroke="{COLORS['navy']}" stroke-width="7"/><polygon points="960,660 949,638 971,638" fill="{COLORS['navy']}"/>
<line x1="1580" y1="540" x2="960" y2="660" stroke="{COLORS['navy']}" stroke-width="7"/><polygon points="960,660 982,649 982,671" fill="{COLORS['navy']}"/>
<line x1="960" y1="860" x2="960" y2="915" stroke="{COLORS['gold']}" stroke-width="8"/><polygon points="960,915 948,891 972,891" fill="{COLORS['gold']}"/>

<text x="120" y="1035" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['muted']}">Kerangka teori ini menggabungkan Teori Literasi Awal, Simple View of Reading, dan Konstruktivisme Sosial Vygotsky sebagai asas konsep kajian.</text>
</svg>"""
    SVG_OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_png()
    build_svg()
    print(PNG_OUT)
    print(SVG_OUT)
