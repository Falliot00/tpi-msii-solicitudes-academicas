import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from solicitudes.cli import main
from solicitudes.inicial import GestorInicial


class ConsolaTest(unittest.TestCase):
    def test_demo_identica_en_ambas_versiones(self) -> None:
        salidas = []
        for version in ["inicial", "refactorizada"]:
            resultado = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "-m",
                    "solicitudes",
                    "--implementacion",
                    version,
                    "demo",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            self.assertEqual(resultado.stderr, "")
            salidas.append(json.loads(resultado.stdout))
        self.assertEqual(salidas[0], salidas[1])
        self.assertEqual(salidas[1]["reporte"]["total"], 1)

    def test_archivo_inicial_es_compatible_con_version_final(self) -> None:
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos.json"
            inicial = GestorInicial(archivo)
            inicial.procesar(
                "registrar",
                estudiante_id=1,
                asunto="Constancia",
                detalle="",
                tipo="constancia",
                prioridad="alta",
            )
            salida = StringIO()
            with redirect_stdout(salida):
                codigo = main(["--archivo", str(archivo), "listar"])
            self.assertEqual(codigo, 0)
            self.assertEqual(json.loads(salida.getvalue()), inicial.procesar("listar"))

    def test_error_de_dominio_y_sin_escritura(self) -> None:
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos.json"
            salida = StringIO()
            with redirect_stderr(salida):
                codigo = main(
                    [
                        "--archivo",
                        str(archivo),
                        "registrar",
                        "--estudiante",
                        "1",
                        "--asunto",
                        " ",
                        "--tipo",
                        "constancia",
                        "--prioridad",
                        "alta",
                    ]
                )
            self.assertEqual(codigo, 2)
            self.assertEqual(json.loads(salida.getvalue()), {"error": "El asunto es obligatorio"})
            self.assertFalse(archivo.exists())

    def test_error_de_persistencia_controlado(self) -> None:
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos.json"
            archivo.write_text("no es JSON", encoding="utf-8")
            salida = StringIO()
            with redirect_stderr(salida):
                codigo = main(["--archivo", str(archivo), "listar"])
            self.assertEqual(codigo, 3)
            self.assertIn("No se pudo leer", json.loads(salida.getvalue())["error"])

    def test_precedencia_de_errores_compatible(self) -> None:
        for version in ["inicial", "refactorizada"]:
            with tempfile.TemporaryDirectory() as carpeta:
                salida = StringIO()
                with redirect_stderr(salida):
                    codigo = main(
                        [
                            "--implementacion",
                            version,
                            "--archivo",
                            str(Path(carpeta) / "datos.json"),
                            "estado",
                            "99",
                            "otro",
                        ]
                    )
                self.assertEqual(codigo, 2)
                self.assertEqual(json.loads(salida.getvalue()), {"error": "Solicitud inexistente"})
