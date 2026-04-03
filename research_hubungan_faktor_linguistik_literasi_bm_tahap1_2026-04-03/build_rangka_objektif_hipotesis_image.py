from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
OUT_DIR = BASE / "figures"
OUT_DIR.mkdir(exist_ok=True)

PNG_OUT = OUT_DIR / "rangka_kajian_objektif_hipotesis.png"
SVG_OUT = OUT_DIR / "rangka_kajian_objektif_hipotesis.svg"

WIDTH = 1920
HEIGHT = 1280

COLORS = {
    "bg": "#F8F6F1",
    "navy": "#104D64",
    "teal": "#1F7A8C",
    "gold": "#D9A441",
    "green": "#5A9466",
    "red": "#B25B53",
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


TITLE_FONT = load_font(42, True)
SUB_FONT = load_font(22, False)
HEAD_FONT = load_font(24, True)
BODY_FONT = load_font(20, False)
SMALL_FONT = load_font(18, False)


def rounded(draw, box, fill, outline, radius=28, width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, box, text, font, fill, spacing=8):
    x1, y1, x2, y2 = box
    lines = text.split("\n")
    bboxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    widths = [b[2] - b[0] for b in bboxes]
    heights = [b[3] - b[1] for b in bboxes]
    total_h = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + (y2 - y1 - total_h) / 2
    for line, w, h in zip(lines, widths, heights):
        x = x1 + (x2 - x1 - w) / 2
        draw.text((x, y), line, font=font, fill=fill)
        y += h + spacing


def arrow(draw, start, end, fill, width=7, head=22):
    draw.line([start, end], fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) > abs(ey - sy):
        if ex >= sx:
            points = [(ex, ey), (ex - head, ey - head / 2), (ex - head, ey + head / 2)]
        else:
            points = [(ex, ey), (ex + head, ey - head / 2), (ex + head, ey + head / 2)]
    else:
        if ey >= sy:
            points = [(ex, ey), (ex - head / 2, ey - head), (ex + head / 2, ey - head)]
        else:
            points = [(ex, ey), (ex - head / 2, ey + head), (ex + head / 2, ey + head)]
    draw.polygon(points, fill=fill)


def build_png():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, 110), fill=COLORS["navy"])
    draw.text((70, 26), "Rangka Kajian: Kaitan antara Objektif Kajian dan Hipotesis Kajian", font=TITLE_FONT, fill=COLORS["white"])
    draw.text((72, 76), "Hubungan aliran objektif deskriptif, objektif inferensi, dan hipotesis yang diuji dalam kajian", font=SUB_FONT, fill="#D8E5EA")

    # Objective boxes
    obj_boxes = {
        "O1": ((110, 180, 840, 300), COLORS["teal"], "Objektif 1\nMengenal pasti tahap faktor linguistik utama murid Tahap 1"),
        "O2": ((110, 335, 840, 455), COLORS["teal"], "Objektif 2\nMengenal pasti strategi pengajaran literasi Bahasa Melayu yang digunakan guru"),
        "O3": ((110, 520, 840, 670), COLORS["gold"], "Objektif 3\nMenentukan hubungan antara faktor linguistik murid dengan keberkesanan strategi pengajaran"),
        "O4": ((110, 1020, 840, 1140), COLORS["green"], "Objektif 4\nMengenal pasti faktor linguistik yang paling dominan meramal keberkesanan strategi pengajaran"),
        "O5": ((110, 1170, 840, 1260), COLORS["navy"], "Objektif 5\nMeneroka bagaimana guru menyesuaikan strategi pengajaran berdasarkan profil linguistik murid"),
    }

    for box, fill, text in obj_boxes.values():
        rounded(draw, box, fill, fill, radius=28, width=1)
        center_text(draw, box, text, HEAD_FONT, COLORS["white"], spacing=6)

    # Hypothesis boxes
    hyp_boxes = {
        "H1": ((1040, 180, 1800, 290), COLORS["white"], COLORS["line"], COLORS["ink"], "H1\nHubungan kesedaran fonologi dengan keberkesanan strategi pengajaran"),
        "H2": ((1040, 320, 1800, 430), COLORS["white"], COLORS["line"], COLORS["ink"], "H2\nHubungan kesedaran morfologi asas dengan keberkesanan strategi pengajaran"),
        "H3": ((1040, 460, 1800, 570), COLORS["white"], COLORS["line"], COLORS["ink"], "H3\nHubungan kosa kata dan bahasa lisan dengan keberkesanan strategi pengajaran"),
        "H4": ((1040, 600, 1800, 710), COLORS["white"], COLORS["line"], COLORS["ink"], "H4\nHubungan bahasa ibunda / bahasa rumah dengan keberkesanan strategi pengajaran"),
        "H5": ((1040, 980, 1800, 1110), COLORS["white"], COLORS["line"], COLORS["ink"], "H5\nFaktor linguistik tertentu merupakan peramal signifikan terhadap keberkesanan strategi pengajaran"),
    }

    for box, fill, outline, text_color, text in hyp_boxes.values():
        rounded(draw, box, fill, outline, radius=28, width=3)
        center_text(draw, box, text, BODY_FONT, text_color, spacing=6)

    # Connectors
    arrow(draw, (840, 240), (1010, 595), COLORS["teal"], width=7, head=20)
    arrow(draw, (840, 395), (1010, 595), COLORS["teal"], width=7, head=20)

    for y in (235, 375, 515, 655):
        arrow(draw, (840, 595), (1040, y), COLORS["gold"], width=7, head=20)

    arrow(draw, (1420, 710), (475, 1020), COLORS["green"], width=7, head=20)
    arrow(draw, (1420, 1110), (475, 1170), COLORS["navy"], width=7, head=20)

    # Labels
    draw.rounded_rectangle((108, 135, 370, 170), radius=18, fill=COLORS["teal"])
    draw.text((142, 142), "Bahagian Objektif Kajian", font=SMALL_FONT, fill=COLORS["white"])
    draw.rounded_rectangle((1038, 135, 1320, 170), radius=18, fill=COLORS["gold"])
    draw.text((1066, 142), "Bahagian Hipotesis Kajian", font=SMALL_FONT, fill=COLORS["white"])

    foot = "O1 dan O2 bersifat deskriptif. O3 diuji melalui H1-H4. O4 diuji melalui H5. O5 melengkapkan dapatan secara kualitatif."
    draw.text((110, 1230), foot, font=SMALL_FONT, fill=COLORS["muted"])

    img.save(PNG_OUT, dpi=(300, 300))


def build_svg():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS['bg']}"/>
<rect x="0" y="0" width="{WIDTH}" height="110" fill="{COLORS['navy']}"/>
<text x="70" y="65" font-family="Arial, Segoe UI, sans-serif" font-size="42" font-weight="700" fill="{COLORS['white']}">Rangka Kajian: Kaitan antara Objektif Kajian dan Hipotesis Kajian</text>
<text x="72" y="96" font-family="Arial, Segoe UI, sans-serif" font-size="22" fill="#D8E5EA">Hubungan aliran objektif deskriptif, objektif inferensi, dan hipotesis yang diuji dalam kajian</text>

<rect x="110" y="180" width="730" height="120" rx="28" fill="{COLORS['teal']}"/>
<rect x="110" y="335" width="730" height="120" rx="28" fill="{COLORS['teal']}"/>
<rect x="110" y="520" width="730" height="150" rx="28" fill="{COLORS['gold']}"/>
<rect x="110" y="1020" width="730" height="120" rx="28" fill="{COLORS['green']}"/>
<rect x="110" y="1170" width="730" height="90" rx="28" fill="{COLORS['navy']}"/>

<text x="475" y="225" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="24" font-weight="700" fill="{COLORS['white']}"><tspan x="475" dy="0">Objektif 1</tspan><tspan x="475" dy="1.35em">Mengenal pasti tahap faktor linguistik utama murid Tahap 1</tspan></text>
<text x="475" y="380" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="24" font-weight="700" fill="{COLORS['white']}"><tspan x="475" dy="0">Objektif 2</tspan><tspan x="475" dy="1.35em">Mengenal pasti strategi pengajaran literasi Bahasa Melayu yang digunakan guru</tspan></text>
<text x="475" y="570" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="24" font-weight="700" fill="{COLORS['white']}"><tspan x="475" dy="0">Objektif 3</tspan><tspan x="475" dy="1.35em">Menentukan hubungan antara faktor linguistik murid</tspan><tspan x="475" dy="1.25em">dengan keberkesanan strategi pengajaran</tspan></text>
<text x="475" y="1065" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="24" font-weight="700" fill="{COLORS['white']}"><tspan x="475" dy="0">Objektif 4</tspan><tspan x="475" dy="1.35em">Mengenal pasti faktor linguistik yang paling dominan meramal keberkesanan strategi pengajaran</tspan></text>
<text x="475" y="1205" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="22" font-weight="700" fill="{COLORS['white']}"><tspan x="475" dy="0">Objektif 5</tspan><tspan x="475" dy="1.3em">Meneroka penyesuaian strategi guru berdasarkan profil linguistik murid</tspan></text>

<rect x="1040" y="180" width="760" height="110" rx="28" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="1040" y="320" width="760" height="110" rx="28" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="1040" y="460" width="760" height="110" rx="28" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="1040" y="600" width="760" height="110" rx="28" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>
<rect x="1040" y="980" width="760" height="130" rx="28" fill="{COLORS['white']}" stroke="{COLORS['line']}" stroke-width="3"/>

<text x="1420" y="220" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['ink']}"><tspan x="1420" dy="0">H1</tspan><tspan x="1420" dy="1.35em">Hubungan kesedaran fonologi dengan keberkesanan strategi pengajaran</tspan></text>
<text x="1420" y="360" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['ink']}"><tspan x="1420" dy="0">H2</tspan><tspan x="1420" dy="1.35em">Hubungan kesedaran morfologi asas dengan keberkesanan strategi pengajaran</tspan></text>
<text x="1420" y="500" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['ink']}"><tspan x="1420" dy="0">H3</tspan><tspan x="1420" dy="1.35em">Hubungan kosa kata dan bahasa lisan dengan keberkesanan strategi pengajaran</tspan></text>
<text x="1420" y="640" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['ink']}"><tspan x="1420" dy="0">H4</tspan><tspan x="1420" dy="1.35em">Hubungan bahasa ibunda / bahasa rumah dengan keberkesanan strategi pengajaran</tspan></text>
<text x="1420" y="1025" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="20" fill="{COLORS['ink']}"><tspan x="1420" dy="0">H5</tspan><tspan x="1420" dy="1.35em">Faktor linguistik tertentu merupakan peramal signifikan</tspan><tspan x="1420" dy="1.25em">terhadap keberkesanan strategi pengajaran</tspan></text>

<line x1="840" y1="240" x2="1010" y2="595" stroke="{COLORS['teal']}" stroke-width="7"/><polygon points="1010,595 990,585 990,605" fill="{COLORS['teal']}"/>
<line x1="840" y1="395" x2="1010" y2="595" stroke="{COLORS['teal']}" stroke-width="7"/><polygon points="1010,595 990,585 990,605" fill="{COLORS['teal']}"/>
<line x1="840" y1="595" x2="1040" y2="235" stroke="{COLORS['gold']}" stroke-width="7"/><polygon points="1040,235 1020,245 1020,225" fill="{COLORS['gold']}"/>
<line x1="840" y1="595" x2="1040" y2="375" stroke="{COLORS['gold']}" stroke-width="7"/><polygon points="1040,375 1020,385 1020,365" fill="{COLORS['gold']}"/>
<line x1="840" y1="595" x2="1040" y2="515" stroke="{COLORS['gold']}" stroke-width="7"/><polygon points="1040,515 1020,525 1020,505" fill="{COLORS['gold']}"/>
<line x1="840" y1="595" x2="1040" y2="655" stroke="{COLORS['gold']}" stroke-width="7"/><polygon points="1040,655 1020,665 1020,645" fill="{COLORS['gold']}"/>
<line x1="1420" y1="710" x2="475" y2="1020" stroke="{COLORS['green']}" stroke-width="7"/><polygon points="475,1020 496,1008 486,1032" fill="{COLORS['green']}"/>
<line x1="1420" y1="1110" x2="475" y2="1170" stroke="{COLORS['navy']}" stroke-width="7"/><polygon points="475,1170 497,1158 487,1182" fill="{COLORS['navy']}"/>

<rect x="108" y="135" width="262" height="35" rx="18" fill="{COLORS['teal']}"/>
<rect x="1038" y="135" width="282" height="35" rx="18" fill="{COLORS['gold']}"/>
<text x="239" y="158" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="18" fill="{COLORS['white']}">Bahagian Objektif Kajian</text>
<text x="1179" y="158" text-anchor="middle" font-family="Arial, Segoe UI, sans-serif" font-size="18" fill="{COLORS['white']}">Bahagian Hipotesis Kajian</text>

<text x="110" y="1230" font-family="Arial, Segoe UI, sans-serif" font-size="18" fill="{COLORS['muted']}">O1 dan O2 bersifat deskriptif. O3 diuji melalui H1-H4. O4 diuji melalui H5. O5 melengkapkan dapatan secara kualitatif.</text>
</svg>"""
    SVG_OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_png()
    build_svg()
    print(PNG_OUT)
    print(SVG_OUT)
