"""Caracterización del comportamiento público previo al refactoring."""

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from typing import Any

from solicitudes.cli import ejecutar
from solicitudes.inicial import GestorInicial
from solicitudes.modulo import ModuloSolicitudes
from solicitudes.repositorios import RepositorioJson, RepositorioMemoria


class ConsolaRefactorizada:
    """Ejercita la interfaz de comandos sin iniciar otro proceso por aserción."""

    def __init__(self, archivo: Path | None = None) -> None:
        self.modulo = ModuloSolicitudes(
            RepositorioMemoria() if archivo is None else RepositorioJson(archivo)
        )

    def procesar(self, accion: str, **datos: Any) -> Any:
        nombres = {
            "estudiante_id": "estudiante",
            "solicitud_id": "id",
            "responsable_id": "responsable",
        }
        argumentos = dict(
            estudiante=0,
            asunto="",
            detalle="",
            tipo="",
            prioridad="",
            id=0,
            responsable=0,
            estado="",
            texto="",
        )
        argumentos.update({nombres.get(k, k): v for k, v in datos.items()})
        return ejecutar(self.modulo, Namespace(comando=accion, **argumentos))


class ContratoInicial(unittest.TestCase):
    def crear_gestor(self, archivo: Path | None = None) -> Any:
        return GestorInicial(archivo)

    def setUp(self) -> None:
        self.gestor = self.crear_gestor()

    def registrar(self, **cambios: Any) -> dict[str, Any]:
        datos = dict(
            estudiante_id=1,
            asunto="  Certificado regular  ",
            detalle=" Beca ",
            tipo="constancia",
            prioridad="alta",
        )
        datos.update(cambios)
        return self.gestor.procesar("registrar", **datos)

    def test_registro_y_normalizacion(self) -> None:
        self.assertEqual(
            self.registrar(),
            {
                "id": 1,
                "estudiante_id": 1,
                "asunto": "Certificado regular",
                "detalle": "Beca",
                "tipo": "constancia",
                "prioridad": "alta",
                "estado": "abierta",
                "responsable_id": None,
            },
        )

    def test_identificadores_correlativos(self) -> None:
        self.registrar()
        self.assertEqual(self.registrar()["id"], 2)

    def test_registros_invalidos_no_se_guardan(self) -> None:
        for cambio, mensaje in [
            ({"estudiante_id": 99}, "Estudiante inexistente"),
            ({"asunto": "  "}, "El asunto es obligatorio"),
            ({"tipo": "otro"}, "Tipo inválido"),
            ({"prioridad": "otra"}, "Prioridad inválida"),
        ]:
            with self.subTest(cambio=cambio):
                with self.assertRaisesRegex(ValueError, mensaje):
                    self.registrar(**cambio)
        self.assertEqual(self.gestor.procesar("listar"), [])

    def test_ciclo_completo(self) -> None:
        self.registrar()
        self.gestor.procesar("asignar", solicitud_id=1, responsable_id=2)
        self.gestor.procesar("estado", solicitud_id=1, estado="en_proceso")
        resultado = self.gestor.procesar("estado", solicitud_id=1, estado="resuelta")
        self.assertEqual(resultado["estado"], "resuelta")
        self.assertEqual(resultado["responsable_id"], 2)

    def test_requiere_responsable(self) -> None:
        self.registrar()
        with self.assertRaisesRegex(ValueError, "Debe asignarse un responsable"):
            self.gestor.procesar("estado", solicitud_id=1, estado="en_proceso")
        self.assertEqual(self.gestor.procesar("listar")[0]["estado"], "abierta")

    def test_impide_salto_y_reapertura(self) -> None:
        self.registrar()
        with self.assertRaisesRegex(ValueError, "Transición de estado no permitida"):
            self.gestor.procesar("estado", solicitud_id=1, estado="resuelta")
        self.gestor.procesar("estado", solicitud_id=1, estado="cancelada")
        with self.assertRaisesRegex(ValueError, "Transición de estado no permitida"):
            self.gestor.procesar("estado", solicitud_id=1, estado="abierta")

    def test_estado_identico_es_idempotente(self) -> None:
        self.registrar()
        self.assertEqual(
            self.gestor.procesar("estado", solicitud_id=1, estado="abierta")["estado"], "abierta"
        )

    def test_impide_asignar_solicitud_cerrada(self) -> None:
        self.registrar()
        self.gestor.procesar("estado", solicitud_id=1, estado="cancelada")
        with self.assertRaisesRegex(ValueError, "Una solicitud cerrada no admite cambios"):
            self.gestor.procesar("asignar", solicitud_id=1, responsable_id=1)

    def test_rechaza_referencias_inexistentes(self) -> None:
        for accion in ["asignar", "estado"]:
            with self.subTest(accion=accion):
                with self.assertRaisesRegex(ValueError, "Solicitud inexistente"):
                    self.gestor.procesar(accion, solicitud_id=99)
        self.registrar()
        with self.assertRaisesRegex(ValueError, "Responsable inexistente"):
            self.gestor.procesar("asignar", solicitud_id=1, responsable_id=99)

    def test_filtros_combinados_y_busqueda(self) -> None:
        self.registrar()
        self.registrar(tipo="equivalencia", prioridad="baja")
        resultado = self.gestor.procesar(
            "listar", estado="abierta", tipo="constancia", prioridad="alta", texto="CERTIFICADO"
        )
        self.assertEqual([s["id"] for s in resultado], [1])
        self.assertEqual(self.gestor.procesar("listar", texto="inexistente"), [])

    def test_filtros_invalidos(self) -> None:
        for campo in ["estado", "tipo", "prioridad"]:
            with self.subTest(campo=campo):
                with self.assertRaises(ValueError):
                    self.gestor.procesar("listar", **{campo: "invalido"})

    def test_reporte_vacio_y_con_datos(self) -> None:
        vacio = {
            "total": 0,
            "por_estado": {"abierta": 0, "en_proceso": 0, "resuelta": 0, "cancelada": 0},
        }
        self.assertEqual(self.gestor.procesar("reporte"), vacio)
        self.registrar()
        self.registrar()
        self.gestor.procesar("estado", solicitud_id=1, estado="cancelada")
        self.assertEqual(
            self.gestor.procesar("reporte"),
            {
                "total": 2,
                "por_estado": {"abierta": 1, "en_proceso": 0, "resuelta": 0, "cancelada": 1},
            },
        )

    def test_persistencia_entre_instancias(self) -> None:
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "solicitudes.json"
            self.gestor = self.crear_gestor(archivo)
            self.registrar()
            otro = self.crear_gestor(archivo)
            self.assertEqual(otro.procesar("listar")[0]["asunto"], "Certificado regular")


class ContratoRefactorizado(ContratoInicial):
    def crear_gestor(self, archivo: Path | None = None) -> Any:
        return ConsolaRefactorizada(archivo)


if __name__ == "__main__":
    unittest.main()
