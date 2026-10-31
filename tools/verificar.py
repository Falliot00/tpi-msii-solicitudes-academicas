"""Ejecutar validaciones y conservar resultados sin ocultar fallos."""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def main() -> int:
    raiz = Path(__file__).resolve().parents[1]
    evidencias = raiz / "docs" / "evidencias"
    evidencias.mkdir(parents=True, exist_ok=True)
    comandos = {
        "suite_completa": [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        "typecheck": [sys.executable, "-m", "mypy"],
        "lint": [sys.executable, "-m", "ruff", "check", "."],
        "formato": [sys.executable, "-m", "ruff", "format", "--check", "."],
        "base_preservada": [
            "git",
            "diff",
            "--exit-code",
            "estado-inicial",
            "--",
            "solicitudes/inicial.py",
        ],
    }
    resultados = {}
    entorno = dict(os.environ, PYTHONUTF8="1")
    for nombre, comando in comandos.items():
        resultado = subprocess.run(
            comando, cwd=raiz, env=entorno, capture_output=True, text=True, encoding="utf-8"
        )
        (evidencias / (nombre + ".txt")).write_text(
            "$ " + " ".join(comando) + "\n" + resultado.stdout + resultado.stderr,
            encoding="utf-8",
        )
        resultados[nombre] = {
            "estado": "PASS" if resultado.returncode == 0 else "FAIL",
            "codigo": resultado.returncode,
        }
        print(nombre + ": " + resultados[nombre]["estado"])
        if resultado.returncode:
            print(resultado.stdout + resultado.stderr)
    demos = []
    for version in ["inicial", "refactorizada"]:
        resultado = subprocess.run(
            [sys.executable, "-m", "solicitudes", "--implementacion", version, "demo"],
            cwd=raiz,
            env=entorno,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        (evidencias / ("demo_" + version + ".json")).write_text(resultado.stdout, encoding="utf-8")
        demos.append((resultado.returncode, resultado.stdout))
    coincide = demos[0][0] == demos[1][0] == 0 and demos[0][1] == demos[1][1]
    resultados["demo_equivalente"] = {
        "estado": "PASS" if coincide else "FAIL",
        "codigo": 0 if coincide else 1,
    }
    reporte = {
        "fecha": datetime.now(timezone(timedelta(hours=-3))).isoformat(),
        "python": sys.version,
        "resultados": resultados,
        "react_doctor": "NO APLICA: no hay React ni Next.js",
    }
    (evidencias / "validacion.json").write_text(
        json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("demo_equivalente: " + resultados["demo_equivalente"]["estado"])
    return int(any(item["estado"] != "PASS" for item in resultados.values()))


if __name__ == "__main__":
    raise SystemExit(main())
