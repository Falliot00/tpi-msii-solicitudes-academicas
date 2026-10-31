"""Interfaz de consola con salidas JSON para demostrar y comparar versiones."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from solicitudes.catalogos import ESTUDIANTES, RESPONSABLES
from solicitudes.dominio import (
    Estado,
    FiltroSolicitudes,
    NuevaSolicitud,
    Prioridad,
    TipoSolicitud,
    convertir_enum,
)
from solicitudes.inicial import GestorInicial
from solicitudes.modulo import ModuloSolicitudes
from solicitudes.repositorios import ErrorPersistencia, RepositorioJson, RepositorioMemoria


def parser() -> argparse.ArgumentParser:
    raiz = argparse.ArgumentParser(description="Gestión de solicitudes académicas")
    raiz.add_argument(
        "--implementacion", choices=["inicial", "refactorizada"], default="refactorizada"
    )
    raiz.add_argument("--archivo", type=Path, default=Path("datos/solicitudes.json"))
    comandos = raiz.add_subparsers(dest="comando", required=True)
    comandos.add_parser("demo", help="Demostración en memoria, sin modificar archivos")
    comandos.add_parser("catalogos")
    registro = comandos.add_parser("registrar")
    registro.add_argument("--estudiante", type=int, required=True)
    registro.add_argument("--asunto", required=True)
    registro.add_argument("--detalle", default="")
    registro.add_argument("--tipo", required=True)
    registro.add_argument("--prioridad", required=True)
    asignacion = comandos.add_parser("asignar")
    asignacion.add_argument("id", type=int)
    asignacion.add_argument("responsable", type=int)
    estado = comandos.add_parser("estado")
    estado.add_argument("id", type=int)
    estado.add_argument("estado")
    consulta = comandos.add_parser("listar")
    for campo in ["estado", "tipo", "prioridad", "texto"]:
        consulta.add_argument("--" + campo, default="")
    comandos.add_parser("reporte")
    return raiz


def ejecutar(modulo: ModuloSolicitudes | GestorInicial, args: argparse.Namespace) -> object:
    if isinstance(modulo, GestorInicial):
        campos = {
            "registrar": ["estudiante", "asunto", "detalle", "tipo", "prioridad"],
            "asignar": ["id", "responsable"],
            "estado": ["id", "estado"],
            "listar": ["estado", "tipo", "prioridad", "texto"],
            "reporte": [],
        }
        nombres = {
            "estudiante": "estudiante_id",
            "id": "solicitud_id",
            "responsable": "responsable_id",
        }
        return modulo.procesar(
            args.comando,
            **{nombres.get(campo, campo): getattr(args, campo) for campo in campos[args.comando]},
        )
    if args.comando == "registrar":
        solicitud = modulo.registrar(
            NuevaSolicitud.desde_textos(
                args.estudiante,
                args.asunto,
                args.detalle,
                args.tipo,
                args.prioridad,
            )
        )
        return solicitud.a_registro()
    if args.comando == "asignar":
        return modulo.asignar(args.id, args.responsable).a_registro()
    if args.comando == "estado":
        return modulo.cambiar_estado(args.id, args.estado).a_registro()
    if args.comando == "listar":
        filtro = FiltroSolicitudes(
            convertir_enum(Estado, args.estado, "Estado inválido") if args.estado else None,
            convertir_enum(TipoSolicitud, args.tipo, "Tipo inválido") if args.tipo else None,
            convertir_enum(Prioridad, args.prioridad, "Prioridad inválida")
            if args.prioridad
            else None,
            args.texto,
        )
        return [s.a_registro() for s in modulo.buscar(filtro)]
    return modulo.reporte()


def demo(implementacion: str) -> object:
    modulo = (
        GestorInicial() if implementacion == "inicial" else ModuloSolicitudes(RepositorioMemoria())
    )
    resultados: dict[str, object] = {}
    comandos = [
        [
            "registrar",
            "--estudiante",
            "1",
            "--asunto",
            "Certificado regular",
            "--detalle",
            "Para beca",
            "--tipo",
            "constancia",
            "--prioridad",
            "alta",
        ],
        ["asignar", "1", "1"],
        ["estado", "1", "en_proceso"],
        ["listar", "--estado", "en_proceso"],
        ["reporte"],
    ]
    for comando in comandos:
        resultados[comando[0]] = ejecutar(modulo, parser().parse_args(comando))
    return resultados


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.comando == "demo":
            resultado = demo(args.implementacion)
        elif args.comando == "catalogos":
            resultado = {
                "estudiantes": [asdict(e) for e in ESTUDIANTES],
                "responsables": [asdict(r) for r in RESPONSABLES],
            }
        else:
            modulo = (
                GestorInicial(args.archivo)
                if args.implementacion == "inicial"
                else ModuloSolicitudes(RepositorioJson(args.archivo))
            )
            resultado = ejecutar(modulo, args)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (ErrorPersistencia, OSError, UnicodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 3
