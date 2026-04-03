from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
OUT_DIR = BASE / "figures"
OUT_DIR.mkdir(exist_ok=True)

PNG_OUT = OUT_DIR / "kerangka_kajian_iv_dv.png"
SVG_OUT = OUT_DIR / "kerangka_kajian_iv_dv.svg"

WIDTH = 1920
HEIGHT = 1080

COLORS = {
    "bg": "#F8F6F1",
    "navy": "#104D64",
    "teal": "#1F7A8C",
    "gold": "#D9A441",
    "ink": "#1F2933",
    "muted": "#5D6C7A",
    "line": "#D5DDE3",
    "white": "#FFFFFF",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                r"C:\Windows\Fonts\arialbd.ttf",
                r"C:\Windows\Fonts\segoeuib.ttf",
                r"C:\Windows\Fonts\calibrib.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                r"C:\Windows\Fonts\arial.ttf",
                r"C:\Windows\Fonts\segoeui.ttf",
                r"C:\Windows\Fonts\calibri.ttf",
            ]
        )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


TITLE_FONT = load_font(44, bold=True)
SUBTITLE_FONT = load_font(24, bold=False)
HEADER_FONT = load_font(28, bold=True)
BODY_FONT = load_font(24, bold=False)
SMALL_FONT = load_font(20, bold=False)


def rounded_box(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_centered_multiline(draw, box, text, font, fill, spacing=10):
    x1, y1, x2, y2 = box
    lines = text.split("\n")
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])
    total_height = sum(line_heights) + spacing * (len(lines) - 1)
    current_y = y1 + ((y2 - y1) - total_height) / 2
    for line, w, h in zip(lines, line_widths, line_heights):
        current_x = x1 + ((x2 - x1) - w) / 2
        draw.text((current_x, current_y), line, font=font, fill=fill)
        current_y += h + spacing


def draw_left_aligned_multiline(draw, box, text, font, fill, spacing=10, bullet=False):
    x1, y1, x2, y2 = box
    current_y = y1
    for raw_line in text.split("\n"):
        line = f"• {raw_line}" if bullet and raw_line.strip() else raw_line
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        draw.text((x1, current_y), line, font=font, fill=fill)
        current_y += height + spacing
        if current_y > y2:
            break


def arrow(draw, start, end, fill, width=8, head=22):
    draw.line([start, end], fill=fill, width=width)
    ex, ey = end
    sx, sy = start
    if ex >= sx:
        points = [(ex, ey), (ex - head, ey - head / 2), (ex - head, ey + head / 2)]
    else:
        points = [(ex, ey), (ex + head, ey - head / 2), (ex + head, ey + head / 2)]
    draw.polygon(points, fill=fill)


def build_png():
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, WIDTH, 120), fill=COLORS["navy"])
    draw.text((80, 30), "Kerangka Kajian Mengikut IV dan DV", font=TITLE_FONT, fill=COLORS["white"])
    draw.text(
        (82, 84),
        "Hubungan antara faktor linguistik murid dengan keberkesanan strategi pengajaran literasi Bahasa Melayu murid Tahap 1",
        font=SUBTITLE_FONT,
        fill="#D8E5EA",
    )

    iv_group = (110, 210, 840, 900)
    dv_group = (1080, 320, 1810, 790)

    rounded_box(draw, iv_group, 36, COLORS["white"], outline=COLORS["line"], width=3)
    rounded_box(draw, dv_group, 36, COLORS["white"], outline=COLORS["line"], width=3)

    draw.rounded_rectangle((110, 170, 470, 230), radius=24, fill=COLORS["teal"])
    draw.text((150, 185), "Pemboleh Ubah Bebas (IV)", font=HEADER_FONT, fill=COLORS["white"])

    draw.rounded_rectangle((1080, 280, 1510, 340), radius=24, fill=COLORS["gold"])
    draw.text((1120, 295), "Pemboleh Ubah Bersandar (DV)", font=HEADER_FONT, fill=COLORS["white"])

    iv_boxes = [
        ((170, 270, 780, 390), "Kesedaran fonologi"),
        ((170, 430, 780, 550), "Kesedaran morfologi asas"),
        ((170, 590, 780, 710), "Kosa kata dan bahasa lisan"),
        ((170, 750, 780, 870), "Bahasa ibunda / bahasa rumah"),
    ]

    for box, label in iv_boxes:
        rounded_box(draw, box, 28, "#F9FBFC", outline=COLORS["line"], width=3)
        draw_centered_multiline(draw, box, label, HEADER_FONT, COLORS["ink"], spacing=8)

    rounded_box(draw, (1145, 395, 1745, 715), 32, "#FFFDF8", outline=COLORS["line"], width=3)
    draw_left_aligned_multiline(
        draw,
        (1195, 455, 1685, 690),
        "Ketepatan bacaan\nKelancaran bacaan\nKefahaman bacaan\nPenulisan asas",
        BODY_FONT,
        COLORS["ink"],
        spacing=22,
        bullet=True,
    )
    draw.text((1195, 405), "Keberkesanan strategi pengajaran literasi Bahasa Melayu", font=HEADER_FONT, fill=COLORS["navy"])

    for box, _label in iv_boxes:
        x1, y1, x2, y2 = box
        arrow(draw, (x2 + 15, (y1 + y2) // 2), (1035, 555), COLORS["teal"], width=7, head=24)

    arrow(draw, (840, 555), (1080, 555), COLORS["navy"], width=10, head=28)

    foot = "Rajah menunjukkan bahawa faktor linguistik murid sebagai IV mempunyai hubungan dengan keberkesanan strategi pengajaran literasi Bahasa Melayu sebagai DV."
    draw.text((120, 970), foot, font=SMALL_FONT, fill=COLORS["muted"])

    image.save(PNG_OUT, dpi=(300, 300))


def svg_rect(x, y, w, h, fill, stroke, rx=28, stroke_width=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def svg_text(x, y, text, size, fill, weight="400", anchor="start"):
    lines = escape(text).split("\n")
    spans = []
    for idx, line in enumerate(lines):
        dy = "0" if idx == 0 else "1.35em"
        spans.append(f'<tspan x="{x}" dy="{dy}">{line}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Segoe UI, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{"".join(spans)}</text>'
    )


def build_svg():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS["bg"]}"/>',
        f'<rect x="0" y="0" width="{WIDTH}" height="120" fill="{COLORS["navy"]}"/>',
        svg_text(80, 62, "Kerangka Kajian Mengikut IV dan DV", 44, COLORS["white"], weight="700"),
        svg_text(
            82,
            96,
            "Hubungan antara faktor linguistik murid dengan keberkesanan strategi pengajaran literasi Bahasa Melayu murid Tahap 1",
            24,
            "#D8E5EA",
        ),
        svg_rect(110, 210, 730, 690, COLORS["white"], COLORS["line"], rx=36),
        svg_rect(1080, 320, 730, 470, COLORS["white"], COLORS["line"], rx=36),
        svg_rect(110, 170, 360, 60, COLORS["teal"], COLORS["teal"], rx=24),
        svg_rect(1080, 280, 430, 60, COLORS["gold"], COLORS["gold"], rx=24),
        svg_text(290, 208, "Pemboleh Ubah Bebas (IV)", 28, COLORS["white"], weight="700", anchor="middle"),
        svg_text(1295, 318, "Pemboleh Ubah Bersandar (DV)", 28, COLORS["white"], weight="700", anchor="middle"),
    ]

    iv_boxes = [
        (170, 270, 610, 120, "Kesedaran fonologi"),
        (170, 430, 610, 120, "Kesedaran morfologi asas"),
        (170, 590, 610, 120, "Kosa kata dan bahasa lisan"),
        (170, 750, 610, 120, "Bahasa ibunda / bahasa rumah"),
    ]
    for x, y, w, h, label in iv_boxes:
        parts.append(svg_rect(x, y, w, h, "#F9FBFC", COLORS["line"]))
        parts.append(svg_text(x + w / 2, y + 68, label, 28, COLORS["ink"], weight="700", anchor="middle"))

    parts.append(svg_rect(1145, 395, 600, 320, "#FFFDF8", COLORS["line"], rx=32))
    parts.append(svg_text(1195, 445, "Keberkesanan strategi pengajaran\nliterasi Bahasa Melayu", 28, COLORS["navy"], weight="700"))
    parts.append(svg_text(1195, 510, "• Ketepatan bacaan\n• Kelancaran bacaan\n• Kefahaman bacaan\n• Penulisan asas", 24, COLORS["ink"]))

    for _x, y, w, h, _label in iv_boxes:
        mid_y = y + h / 2
        parts.append(
            f'<line x1="{170 + w + 15}" y1="{mid_y}" x2="1035" y2="555" stroke="{COLORS["teal"]}" stroke-width="7"/>'
        )
        parts.append(
            f'<polygon points="1035,555 1011,543 1011,567" fill="{COLORS["teal"]}"/>'
        )
    parts.append(f'<line x1="840" y1="555" x2="1080" y2="555" stroke="{COLORS["navy"]}" stroke-width="10"/>')
    parts.append(f'<polygon points="1080,555 1052,541 1052,569" fill="{COLORS["navy"]}"/>')
    parts.append(
        svg_text(
            120,
            995,
            "Rajah menunjukkan bahawa faktor linguistik murid sebagai IV mempunyai hubungan dengan keberkesanan strategi pengajaran literasi Bahasa Melayu sebagai DV.",
            20,
            COLORS["muted"],
        )
    )
    parts.append("</svg>")
    SVG_OUT.write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    build_png()
    build_svg()
    print(PNG_OUT)
    print(SVG_OUT)
