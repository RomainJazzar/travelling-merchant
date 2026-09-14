"""Convertit les livrables Markdown du dossier de soutenance en PDF.

    python tools/md_to_pdf.py FICHIER.md [SORTIE.pdf]
    python tools/md_to_pdf.py --all

Gère : titres, paragraphes, **gras**, *italique*, `code`, listes à puces et
numérotées, tableaux, blocs de code, citations et filets horizontaux.

Les polices DejaVu (fournies avec matplotlib) sont utilisées pour couvrir les
symboles mathématiques : ≤ ≥ ≈ → σ φ λ Δ ∎ …
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent

# --- Polices --------------------------------------------------------------
FONT_DIR = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
for name, filename in [
    ("DejaVu", "DejaVuSans.ttf"),
    ("DejaVu-Bold", "DejaVuSans-Bold.ttf"),
    ("DejaVu-Italic", "DejaVuSans-Oblique.ttf"),
    ("DejaVu-BoldItalic", "DejaVuSans-BoldOblique.ttf"),
    ("DejaVuMono", "DejaVuSansMono.ttf"),
    ("DejaVuMono-Bold", "DejaVuSansMono-Bold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily(
    "DejaVu", normal="DejaVu", bold="DejaVu-Bold",
    italic="DejaVu-Italic", boldItalic="DejaVu-BoldItalic")

# --- Palette (version claire de la charte) --------------------------------
INK = colors.HexColor("#111827")
BODY = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#5B6B84")
GOLD = colors.HexColor("#A9761F")
NAVY = colors.HexColor("#14304F")
CYAN = colors.HexColor("#136A82")
RULE = colors.HexColor("#D7DEE8")
BAND = colors.HexColor("#F1F5FA")
CODEBG = colors.HexColor("#F5F7FA")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


def _style(name, **kw):
    base = dict(fontName="DejaVu", fontSize=9.4, leading=13.6, textColor=BODY,
                alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h1": _style("h1", fontName="DejaVu-Bold", fontSize=19, leading=23,
                 textColor=NAVY, spaceBefore=16, spaceAfter=8),
    "h2": _style("h2", fontName="DejaVu-Bold", fontSize=14.5, leading=18.5,
                 textColor=NAVY, spaceBefore=13, spaceAfter=6),
    "h3": _style("h3", fontName="DejaVu-Bold", fontSize=11.4, leading=15,
                 textColor=GOLD, spaceBefore=10, spaceAfter=4),
    "h4": _style("h4", fontName="DejaVu-Bold", fontSize=10, leading=13.5,
                 textColor=CYAN, spaceBefore=8, spaceAfter=3),
    "p": _style("p", spaceAfter=5),
    "li": _style("li", leftIndent=11, bulletIndent=2, spaceAfter=2.4),
    "quote": _style("quote", leftIndent=9, rightIndent=5, textColor=NAVY,
                    fontName="DejaVu-Italic", spaceBefore=4, spaceAfter=6),
    "code": _style("code", fontName="DejaVuMono", fontSize=7.9, leading=10.6,
                   textColor=INK),
    "cell": _style("cell", fontSize=8.1, leading=11),
    "cellh": _style("cellh", fontName="DejaVu-Bold", fontSize=8.1, leading=11,
                    textColor=NAVY),
    "title": _style("title", fontName="DejaVu-Bold", fontSize=26, leading=31,
                    textColor=NAVY, alignment=TA_CENTER),
    "subtitle": _style("subtitle", fontSize=12, leading=17, textColor=MUTED,
                       alignment=TA_CENTER),
}


# --- Conversion des enrichissements en ligne ------------------------------
def emphasis(text: str) -> str:
    """Traduit ** et * en <b>/<i> avec une pile, donc toujours bien imbriqués.

    Une expression régulière ne suffit pas : des séquences comme
    `**gras *ital***` mélangent les marqueurs et produiraient des balises
    croisées, que ReportLab refuse.
    """
    out: list[str] = []
    open_tags: list[str] = []

    def close(tag: str) -> None:
        """Ferme `tag` en refermant proprement ce qui est ouvert au-dessus."""
        if tag not in open_tags:
            return
        above = open_tags[open_tags.index(tag) + 1:]
        for t in reversed(above):
            out.append(f"</{t}>")
        out.append(f"</{tag}>")
        open_tags.remove(tag)
        for t in above:
            out.append(f"<{t}>")

    def toggle(tag: str) -> None:
        if tag in open_tags:
            close(tag)
        else:
            open_tags.append(tag)
            out.append(f"<{tag}>")

    for token in re.split(r"(\*{1,3})", text):
        if token == "***":
            # Ouvre les deux, ou ferme les deux, selon l'état courant.
            if "b" in open_tags and "i" in open_tags:
                close("i")
                close("b")
            else:
                toggle("b")
                toggle("i")
        elif token == "**":
            toggle("b")
        elif token == "*":
            toggle("i")
        elif token:
            out.append(token)

    for tag in reversed(open_tags):
        out.append(f"</{tag}>")
    return "".join(out)


def inline(text: str) -> str:
    """Traduit le Markdown inline en balises ReportLab."""
    out, codes = [], []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)      # liens : texte seul
    text = emphasis(text)

    def unstash(m):
        code = html.escape(codes[int(m.group(1))], quote=False)
        return (f'<font face="DejaVuMono" size="8.4" color="#8A4B1A">'
                f'{code}</font>')

    return re.sub(r"\x00(\d+)\x00", unstash, text)


def P(text: str, style, **kw) -> Paragraph:
    """Paragraphe tolerant : si le balisage genere echoue, on retombe sur du
    texte brut plutot que de faire echouer tout le document."""
    try:
        return Paragraph(text, style, **kw)
    except Exception:
        plain = html.escape(re.sub(r"<[^>]+>", "", text), quote=False)
        return Paragraph(plain, style, **kw)


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip())) and "-" in line


def build_table(rows: list[list[str]], avail: float) -> Table:
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]

    # Largeurs proportionnelles au contenu, bornées pour rester lisibles.
    weights = []
    for c in range(ncols):
        longest = max(len(re.sub(r"[*`]", "", r[c])) for r in rows)
        weights.append(max(min(longest, 60), 6))
    total = sum(weights)
    widths = [avail * w / total for w in weights]

    data = [[P(inline(c), S["cellh" if i == 0 else "cell"])
             for c in row] for i, row in enumerate(rows)]

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), BAND),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, NAVY),
        ("LINEBELOW", (0, 1), (-1, -2), 0.35, RULE),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for r in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FAFBFD")))
    t.setStyle(TableStyle(style))
    return t


def parse(md: str, avail: float) -> list:
    flow, lines, i = [], md.split("\n"), 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Bloc de code
        if stripped.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            body = "\n".join(buf).rstrip()
            if body:
                pre = Preformatted(body, S["code"])
                t = Table([[pre]], colWidths=[avail], hAlign="LEFT")
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                    ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))
                flow += [Spacer(1, 3), t, Spacer(1, 7)]
            continue

        # Tableau
        if stripped.startswith("|") and i + 1 < n and is_separator(lines[i + 1]):
            rows = [split_row(stripped)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            flow += [Spacer(1, 3), build_table(rows, avail), Spacer(1, 8)]
            continue

        # Filet horizontal
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            flow += [Spacer(1, 7),
                     HRFlowable(width="100%", thickness=0.7, color=RULE),
                     Spacer(1, 7)]
            i += 1
            continue

        # Image seule sur sa ligne : ![légende](chemin)
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if m:
            caption, rel = m.group(1), m.group(2)
            path = (ROOT / "FINAL_SOUTENANCE" / rel).resolve()
            if path.exists():
                from PIL import Image as PILImage
                from reportlab.platypus import Image as RLImage
                with PILImage.open(path) as im:
                    iw, ih = im.size
                w = min(avail, 165 * mm)
                h = w * ih / iw
                max_h = 195 * mm
                if h > max_h:
                    h, w = max_h, max_h * iw / ih
                block = [RLImage(str(path), width=w, height=h)]
                if caption:
                    block += [Spacer(1, 3),
                              P(inline(caption),
                                _style("cap", fontSize=8.4, leading=11.5,
                                       textColor=MUTED, alignment=TA_CENTER))]
                flow += [Spacer(1, 6), KeepTogether(block), Spacer(1, 10)]
            i += 1
            continue

        # Titres
        m = re.match(r"^(#{1,4})\s+(.*)", stripped)
        if m:
            level = len(m.group(1))
            para = P(inline(m.group(2)), S[f"h{level}"])
            flow.append(para if level > 1 else KeepTogether([para]))
            if level == 1:
                flow.append(HRFlowable(width="100%", thickness=1.1, color=GOLD,
                                       spaceAfter=7))
            i += 1
            continue

        # Citation
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            text = " ".join(x for x in buf if x)
            if text:
                p = P(inline(text), S["quote"])
                t = Table([[p]], colWidths=[avail], hAlign="LEFT")
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), BAND),
                    ("LINEBEFORE", (0, 0), (0, -1), 2.2, GOLD),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                flow += [Spacer(1, 3), t, Spacer(1, 7)]
            continue

        # Listes
        m = re.match(r"^([-*+]|\d+\.)\s+(.*)", stripped)
        if m:
            while i < n:
                cur = lines[i].strip()
                mm_ = re.match(r"^([-*+]|\d+\.)\s+(.*)", cur)
                if not mm_:
                    break
                marker = "•" if mm_.group(1) in "-*+" else mm_.group(1)
                body = mm_.group(2)
                i += 1
                # continuation indentée
                while i < n and lines[i].startswith(("   ", "\t")) \
                        and lines[i].strip() \
                        and not re.match(r"^([-*+]|\d+\.)\s", lines[i].strip()):
                    body += " " + lines[i].strip()
                    i += 1
                flow.append(P(inline(body), S["li"], bulletText=marker))
            flow.append(Spacer(1, 5))
            continue

        # Ligne vide
        if not stripped:
            i += 1
            continue

        # Paragraphe
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|\||>|```|[-*+]\s|\d+\.\s|-{3,}$)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            flow.append(P(inline(" ".join(buf)), S["p"]))
    return flow


def cover(title: str, subtitle: str, avail: float) -> list:
    return [
        Spacer(1, 55 * mm),
        Paragraph(title, S["title"]),
        Spacer(1, 6 * mm),
        HRFlowable(width="38%", thickness=2, color=GOLD, hAlign="CENTER"),
        Spacer(1, 6 * mm),
        Paragraph(subtitle, S["subtitle"]),
        Spacer(1, 14 * mm),
        Paragraph("Romain &nbsp;·&nbsp; Yannis &nbsp;·&nbsp; Lisa", S["subtitle"]),
        Spacer(1, 2 * mm),
        Paragraph("github.com/RomainJazzar/travelling-merchant", S["subtitle"]),
        PageBreak(),
    ]


def make_pdf(src: Path, dest: Path, title: str | None = None,
             subtitle: str = "") -> None:
    md = src.read_text(encoding="utf-8")

    # Le premier titre de niveau 1 sert de couverture.
    lines = md.split("\n")
    if title is None:
        title = next((l.lstrip("# ").strip() for l in lines
                      if l.startswith("# ")), src.stem)
        for idx, l in enumerate(lines):
            if l.startswith("# "):
                lines = lines[idx + 1:]
                break
        md = "\n".join(lines)

    avail = PAGE_W - 2 * MARGIN
    doc = BaseDocTemplate(
        str(dest), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN + 6 * mm,
        title=title, author="Romain, Yannis & Lisa")

    frame = Frame(MARGIN, MARGIN + 6 * mm, avail,
                  PAGE_H - 2 * MARGIN - 6 * mm, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def decorate(canvas, _doc):
        canvas.saveState()
        if canvas.getPageNumber() > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.5)
            canvas.line(MARGIN, MARGIN + 4 * mm, PAGE_W - MARGIN, MARGIN + 4 * mm)
            canvas.setFont("DejaVu", 7.4)
            canvas.setFillColor(MUTED)
            canvas.drawString(MARGIN, MARGIN - 1 * mm,
                              "Le marchand ambulant · TSP · Romain, Yannis & Lisa")
            canvas.drawRightString(PAGE_W - MARGIN, MARGIN - 1 * mm,
                                   str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="std", frames=[frame],
                                       onPage=decorate)])
    story = cover(title, subtitle, avail) + parse(md, avail)
    doc.build(story)
    print(f"  ✓ {dest}  ({dest.stat().st_size // 1024} Ko)")


DOCS = [
    ("GUIDE_DEFENSE_ORAL_TRAVELLING_MERCHANT.md",
     "Guide de défense orale",
     "Comprendre, expliquer et défendre le projet de A à Z"),
    ("QUESTIONS_PROF_100_PLUS.md",
     "172 questions du professeur",
     "Réponse courte, réponse développée, erreur à éviter"),
    ("SCRIPT_ORAL_ROMAIN_YANNIS_LISA.md",
     "Script de soutenance",
     "19 slides · répartition, minutage et transitions"),
    ("FICHE_REVISION_ULTIME.md",
     "Fiche de révision ultime",
     "À relire 10 minutes avant l'oral"),
]


def main() -> None:
    base = ROOT / "FINAL_SOUTENANCE"
    if "--all" in sys.argv:
        print("Génération des PDF :")
        for name, title, subtitle in DOCS:
            make_pdf(base / name, base / name.replace(".md", ".pdf"),
                     title, subtitle)
        return
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    make_pdf(src, dest)


if __name__ == "__main__":
    main()
