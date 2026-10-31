"""Crear un panel documental para capturar salidas reales de las herramientas."""

import html
import json
from pathlib import Path


def main() -> None:
    evidencias = Path(__file__).resolve().parents[1] / "docs" / "evidencias"
    cuadros = []
    for version in ["inicial", "refactorizada"]:
        fuente = "demo_" + version + ".json"
        datos = json.loads((evidencias / fuente).read_text(encoding="utf-8"))
        salida = html.escape(json.dumps(datos["listar"], ensure_ascii=False, indent=2))
        cuadros.append(
            f"<article><h2>{version.title()}</h2><p>{fuente}</p><pre>{salida}</pre></article>"
        )
    v = json.loads((evidencias / "validacion.json").read_text(encoding="utf-8"))
    filas = "".join(
        "<tr><td>"
        + html.escape(n)
        + "</td><td>"
        + r["estado"]
        + "</td><td>"
        + str(r["codigo"])
        + "</td></tr>"
        for n, r in v["resultados"].items()
    )
    resumen = (evidencias / "suite_completa.txt").read_text(encoding="utf-8").splitlines()[-5:]
    documento = """<!doctype html><html lang="es"><meta charset="utf-8">
<title>Evidencias ejecutadas del TPI</title><style>
*{box-sizing:border-box}body{margin:0;background:#e8edf1;color:#172c46;font:18px Arial}
section{width:1100px;padding:28px;background:white;margin:0 0 24px}h1{font-size:28px;margin:0 0 12px}
h2{font-size:23px;margin:0 0 8px}p{font-size:16px;margin:0 0 18px}.grid{display:flex;gap:24px}
article{flex:1;min-width:0;background:#f2f6f8;padding:20px}pre{font:17px/1.45 Consolas,monospace;margin:0}
table{width:100%;border-collapse:collapse;margin:18px 0}td,th{padding:9px;text-align:left;border-bottom:1px solid #d9e3e8}
th{background:#dfedef}td:nth-child(2){font-weight:bold;color:#14655a}.nota{margin-top:12px;color:#526578}
</style><body><section id="demo"><h1>E07 Comparación de la salida ejecutada</h1>
<p>Resultado de listar después de registrar, asignar y pasar a en_proceso.</p><div class="grid">"""
    documento += (
        "".join(cuadros)
        + "</div><p class='nota'>Panel documental a partir de logs; el producto funciona por consola.</p></section>"
    )
    documento += (
        "<section id='validacion'><h1>E08 Verificación ejecutada</h1><p>"
        + html.escape(v["fecha"])
        + "</p>"
    )
    documento += (
        "<table><tr><th>Comprobación</th><th>Resultado</th><th>Código</th></tr>"
        + filas
        + "</table>"
    )
    documento += (
        "<pre>"
        + html.escape("\n".join(resumen))
        + "</pre><p class='nota'>Fuentes: validacion.json y suite_completa.txt</p></section></body></html>"
    )
    (evidencias / "panel.html").write_text(documento, encoding="utf-8")
    print(evidencias / "panel.html")


if __name__ == "__main__":
    main()
