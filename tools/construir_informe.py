"""Generar el informe PDF desde su fuente editable y resultados ejecutados."""

import html
import json
import re
import textwrap
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ = Path(__file__).resolve().parents[1]
AZUL = colors.HexColor("#172C46")
VERDE = colors.HexColor("#14756F")


def fuentes() -> tuple[str, str, str]:
    carpeta = Path("C:/Windows/Fonts")
    if (carpeta / "segoeui.ttf").exists():
        for nombre, archivo in [
            ("Texto", "segoeui.ttf"),
            ("TextoBold", "segoeuib.ttf"),
            ("Codigo", "consola.ttf"),
        ]:
            pdfmetrics.registerFont(TTFont(nombre, str(carpeta / archivo)))
        pdfmetrics.registerFontFamily(
            "Texto", normal="Texto", bold="TextoBold", italic="Texto", boldItalic="TextoBold"
        )
        return "Texto", "TextoBold", "Codigo"
    return "Helvetica", "Helvetica-Bold", "Courier"


FUENTE_CODIGO = "Courier"
VINETA = re.compile(r"^(- |\d+\. )")


def markup(texto: str) -> str:
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(texto))
    return re.sub(r"`([^`]+)`", r'<font name="' + FUENTE_CODIGO + r'">\1</font>', texto)


def diagrama(fuente: str) -> Drawing:
    dibujo = Drawing(467, 146)
    cajas = [
        (0, 103, 110, "Consola JSON"),
        (165, 103, 137, "Módulo de solicitudes"),
        (354, 103, 110, "Dominio"),
        (165, 47, 137, "Contrato repositorio"),
        (70, 0, 125, "Memoria"),
        (275, 0, 125, "Archivo JSON"),
    ]
    for x, y, ancho, titulo in cajas:
        dibujo.add(
            Rect(
                x,
                y,
                ancho,
                34,
                fillColor=colors.HexColor("#EAF2F3"),
                strokeColor=VERDE,
                strokeWidth=0.6,
                rx=4,
                ry=4,
            )
        )
        dibujo.add(
            String(
                x + ancho / 2,
                y + 13,
                titulo,
                textAnchor="middle",
                fontName=fuente,
                fontSize=8.5,
                fillColor=AZUL,
            )
        )
    for x1, y1, x2, y2 in [
        (110, 120, 165, 120),
        (302, 120, 354, 120),
        (233, 103, 233, 81),
        (205, 47, 132, 34),
        (260, 47, 337, 34),
    ]:
        dibujo.add(Line(x1, y1, x2, y2, strokeColor=VERDE, strokeWidth=1))
    return dibujo


def main() -> None:
    global FUENTE_CODIGO
    normal, negrita, mono = fuentes()
    FUENTE_CODIGO = mono
    cuerpo = ParagraphStyle(
        "Cuerpo", fontName=normal, fontSize=10.1, leading=14.5, textColor=AZUL, spaceAfter=9
    )
    item_lista = ParagraphStyle(
        "ItemLista",
        parent=cuerpo,
        leftIndent=18,
        bulletIndent=4,
        spaceAfter=3,
        bulletFontName="Helvetica",
        bulletFontSize=9,
    )
    item_numerado = ParagraphStyle(
        "ItemNumerado", parent=item_lista, bulletFontName=normal, bulletFontSize=10.1
    )
    titulo = ParagraphStyle(
        "Titulo",
        parent=cuerpo,
        fontName=negrita,
        fontSize=19,
        leading=24,
        spaceAfter=17,
        keepWithNext=True,
    )
    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=cuerpo,
        fontName=negrita,
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=7,
        keepWithNext=True,
    )
    celda = ParagraphStyle("Celda", parent=cuerpo, fontSize=8.3, leading=11.7, spaceAfter=0)
    codigo = ParagraphStyle(
        "Codigo",
        fontName=mono,
        fontSize=8,
        leading=11,
        leftIndent=7,
        spaceBefore=4,
        spaceAfter=12,
        backColor=colors.HexColor("#F1F4F7"),
    )
    config = json.loads((RAIZ / "config_entrega.json").read_text(encoding="utf-8"))
    elementos = [
        Spacer(1, 46),
        Paragraph("Trabajo Práctico Integrador", titulo),
        Paragraph("Metodología de Sistemas 2", subtitulo),
        Spacer(1, 30),
        Paragraph(
            "Calidad y evolución de un sistema de solicitudes académicas",
            ParagraphStyle("Portada", parent=titulo, fontSize=28, leading=35),
        ),
        Spacer(1, 28),
        Paragraph("Integrantes:", subtitulo),
        Paragraph(
            "<b>Fermin Alliot</b> · Legajo 101414 · Comisión M25 C4-02<br/><b>Gabriel Antuña</b> · Legajo 100506 · Comisión M25 C4-12",
            cuerpo,
        ),
        Paragraph("Tecnicatura Universitaria en Programación a Distancia", cuerpo),
        Spacer(1, 24),
        Paragraph(config["fecha_informe"], cuerpo),
        Spacer(1, 14),
        Paragraph(
            "Sistema base, diagnóstico, mejoras de diseño, pruebas y revisión técnica", cuerpo
        ),
        Paragraph(
            "Trabajo grupal (2 integrantes) · Asistencia de IA como copiloto declarada", cuerpo
        ),
        PageBreak(),
    ]

    def parrafo(texto: str) -> None:
        elementos.append(Paragraph(markup(texto), cuerpo))

    def item(marcador: str, texto: str) -> None:
        numerado = marcador != "-"
        elementos.append(
            Paragraph(
                markup(texto),
                item_numerado if numerado else item_lista,
                bulletText=marcador if numerado else "•",
            )
        )

    def tabla(filas: list[list[str]]) -> None:
        n = len(filas[0])
        proporciones = {2: [0.28, 0.72], 3: [0.26, 0.51, 0.23], 4: [0.22, 0.30, 0.24, 0.24]}
        datos = [[Paragraph(markup(c), celda) for c in fila] for fila in filas]
        tabla_pdf = Table(
            datos,
            colWidths=[467 * p for p in proporciones.get(n, [1 / n] * n)],
            repeatRows=1,
            hAlign="LEFT",
        )
        tabla_pdf.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDEBED")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#F4F7F9")],
                    ),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.6, VERDE),
                ]
            )
        )
        elementos.extend([tabla_pdf, Spacer(1, 12)])

    lineas = (RAIZ / "docs/informe.md").read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if not linea:
            i += 1
            continue
        if linea == "<!-- salto -->":
            elementos.append(PageBreak())
        elif linea == "<!-- arquitectura -->":
            elementos.extend([diagrama(normal), Spacer(1, 12)])
        elif linea in {"<!-- captura_demo -->", "<!-- captura_validacion -->"}:
            nombre = "captura_demo.jpg" if "captura_demo" in linea else "captura_validacion.jpg"
            captura = Image(str(RAIZ / "docs/evidencias" / nombre))
            captura.drawHeight = captura.imageHeight * 467 / captura.imageWidth
            captura.drawWidth = 467
            elementos.extend([captura, Spacer(1, 9)])
        elif linea == "<!-- validacion -->":
            v = json.loads((RAIZ / "docs/evidencias/validacion.json").read_text(encoding="utf-8"))
            parrafo("Ejecución registrada: " + v["fecha"] + ".")
            tabla(
                [["Comprobación", "Resultado"]]
                + [
                    [n, r["estado"] + " (código " + str(r["codigo"]) + ")"]
                    for n, r in v["resultados"].items()
                ]
            )
        elif linea == "<!-- revision -->":
            ruta = RAIZ / "docs/ia/revision_resultado.json"
            if ruta.exists():
                for eje, resultado in json.loads(ruta.read_text(encoding="utf-8")).items():
                    parrafo(eje + ": " + resultado)
            else:
                parrafo("Revisión por dos ejes pendiente de incorporar al cierre documental.")
        elif linea == "<!-- enlaces -->":
            repo_url = config.get("repositorio_github")
            if repo_url:
                seguro_repo = html.escape(repo_url, quote=True)
                elementos.append(
                    Paragraph(
                        'Repositorio GitHub: <link href="'
                        + seguro_repo
                        + '">'
                        + seguro_repo
                        + "</link>",
                        cuerpo,
                    )
                )
            else:
                parrafo("Repositorio GitHub: disponible en el paquete de entrega.")

            video_url = config.get("video")
            if video_url:
                seguro_vid = html.escape(video_url, quote=True)
                elementos.append(
                    Paragraph(
                        'Video de defensa: <link href="'
                        + seguro_vid
                        + '">'
                        + seguro_vid
                        + "</link>",
                        cuerpo,
                    )
                )
            else:
                parrafo(
                    "Video de defensa: enlace provisto junto a la entrega final en la plataforma de la cátedra / documento anexo."
                )
        elif linea.startswith("```"):
            bloque = []
            i += 1
            while i < len(lineas) and not lineas[i].strip().startswith("```"):
                bloque.extend(
                    textwrap.wrap(
                        lineas[i], width=88, replace_whitespace=False, drop_whitespace=False
                    )
                    or [""]
                )
                i += 1
            elementos.append(Preformatted("\n".join(bloque), codigo))
        elif linea.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", c) for c in celdas):
                    filas.append(celdas)
                i += 1
            tabla(filas)
            continue
        elif linea.startswith("# "):
            elementos.append(Paragraph(markup(linea[2:]), titulo))
        elif linea.startswith("## "):
            elementos.append(Paragraph(markup(linea[3:]), subtitulo))
        elif VINETA.match(linea):
            marcador, texto = linea.split(" ", 1)
            bloque = [texto]
            while (
                i + 1 < len(lineas)
                and lineas[i + 1].strip()
                and not VINETA.match(lineas[i + 1].strip())
                and not lineas[i + 1].startswith(("#", "|", "<!--", "```"))
            ):
                i += 1
                bloque.append(lineas[i].strip())
            item(marcador, " ".join(bloque))
            siguiente = next((x.strip() for x in lineas[i + 1 :] if x.strip()), "")
            if not VINETA.match(siguiente):
                elementos.append(Spacer(1, 6))
        else:
            bloque = [linea]
            while (
                i + 1 < len(lineas)
                and lineas[i + 1].strip()
                and not VINETA.match(lineas[i + 1].strip())
                and not lineas[i + 1].startswith(("#", "|", "<!--", "```"))
            ):
                i += 1
                bloque.append(lineas[i].strip())
            parrafo(" ".join(bloque))
        i += 1

    def pie(canvas: object, documento: object) -> None:
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#607080"))
        canvas.setFont(normal, 8)
        canvas.drawString(
            64, 32, "Fermin Alliot · Gabriel Antuña · Metodología de Sistemas 2 · TPI"
        )
        canvas.drawRightString(A4[0] - 64, 32, str(documento.page))
        canvas.restoreState()

    salida = RAIZ / "entrega/Alliot_Fermin_TPI_MSII.pdf"
    salida.parent.mkdir(exist_ok=True)
    documento = SimpleDocTemplate(
        str(salida),
        pagesize=A4,
        rightMargin=64,
        leftMargin=64,
        topMargin=49,
        bottomMargin=52,
        title="TPI Solicitudes académicas",
        author="Fermin Alliot, Gabriel Antuña",
        subject="Calidad y refactoring seguro",
    )
    documento.build(elementos, onFirstPage=pie, onLaterPages=pie)
    print(salida)


if __name__ == "__main__":
    main()
