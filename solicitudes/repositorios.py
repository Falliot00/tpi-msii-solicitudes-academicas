"""Dos adaptadores para el mismo contrato de almacenamiento local."""

import json
import os
import tempfile
from pathlib import Path
from typing import Protocol

from solicitudes.catalogos import ESTUDIANTES, RESPONSABLES
from solicitudes.dominio import Estado, NuevaSolicitud, Prioridad, Solicitud, TipoSolicitud


class ErrorPersistencia(Exception):
    """No se pudo leer o guardar el archivo de solicitudes."""


class RepositorioSolicitudes(Protocol):
    """Lista en orden de ID, guarda por ID y rechaza obtener un ID ausente.

    Las entidades son inmutables; modificar la lista devuelta no afecta el
    repositorio. guardar inserta o reemplaza un ID. No soporta concurrencia.
    """

    def listar(self) -> list[Solicitud]: ...

    def obtener(self, solicitud_id: int) -> Solicitud: ...

    def guardar(self, solicitud: Solicitud) -> None: ...


class RepositorioMemoria:
    def __init__(self) -> None:
        self._solicitudes: dict[int, Solicitud] = {}

    def listar(self) -> list[Solicitud]:
        return sorted(self._solicitudes.values(), key=lambda s: s.id)

    def obtener(self, solicitud_id: int) -> Solicitud:
        try:
            return self._solicitudes[solicitud_id]
        except KeyError:
            raise ValueError("Solicitud inexistente") from None

    def guardar(self, solicitud: Solicitud) -> None:
        self._solicitudes[solicitud.id] = solicitud


def _entero(valor: object) -> int:
    if type(valor) is not int:
        raise ValueError("Identificador inválido")
    return valor


def _texto(valor: object) -> str:
    if not isinstance(valor, str):
        raise ValueError("Texto inválido")
    return valor


def _desde_registro(valor: object) -> Solicitud:
    if not isinstance(valor, dict):
        raise ValueError("Registro inválido")
    identificador = _entero(valor["id"])
    estudiante_id = _entero(valor["estudiante_id"])
    responsable = valor["responsable_id"]
    responsable_id = None if responsable is None else _entero(responsable)
    if identificador <= 0 or estudiante_id not in {e.id for e in ESTUDIANTES}:
        raise ValueError("Identificador inválido")
    if responsable_id is not None and responsable_id not in {r.id for r in RESPONSABLES}:
        raise ValueError("Responsable inexistente")
    solicitud = Solicitud(
        id=identificador,
        estudiante_id=estudiante_id,
        asunto=_texto(valor["asunto"]),
        detalle=_texto(valor["detalle"]),
        tipo=TipoSolicitud(_texto(valor["tipo"])),
        prioridad=Prioridad(_texto(valor["prioridad"])),
        estado=Estado(_texto(valor["estado"])),
        responsable_id=responsable_id,
    )
    NuevaSolicitud(
        estudiante_id, solicitud.asunto, solicitud.detalle, solicitud.tipo, solicitud.prioridad
    ).validar()
    if solicitud.estado in {Estado.EN_PROCESO, Estado.RESUELTA} and responsable_id is None:
        raise ValueError("Estado sin responsable")
    return solicitud


class RepositorioJson:
    def __init__(self, archivo: Path) -> None:
        self._archivo = archivo

    def _cargar(self) -> RepositorioMemoria:
        memoria = RepositorioMemoria()
        try:
            datos: object = json.loads(self._archivo.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return memoria
        except (OSError, UnicodeError, ValueError) as error:
            raise ErrorPersistencia("No se pudo leer el archivo de solicitudes") from error
        try:
            if not isinstance(datos, list):
                raise ValueError("Se esperaba una lista")
            ids: set[int] = set()
            for dato in datos:
                solicitud = _desde_registro(dato)
                if solicitud.id in ids:
                    raise ValueError("Identificador duplicado")
                ids.add(solicitud.id)
                memoria.guardar(solicitud)
        except (KeyError, TypeError, ValueError) as error:
            raise ErrorPersistencia("Formato inválido del archivo de solicitudes") from error
        return memoria

    def listar(self) -> list[Solicitud]:
        return self._cargar().listar()

    def obtener(self, solicitud_id: int) -> Solicitud:
        return self._cargar().obtener(solicitud_id)

    def guardar(self, solicitud: Solicitud) -> None:
        memoria = self._cargar()
        memoria.guardar(solicitud)
        temporal: Path | None = None
        try:
            self._archivo.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._archivo.parent,
                prefix="solicitudes-",
                suffix=".tmp",
                delete=False,
            ) as salida:
                temporal = Path(salida.name)
                json.dump(
                    [s.a_registro() for s in memoria.listar()], salida, ensure_ascii=False, indent=2
                )
            os.replace(temporal, self._archivo)
        except OSError as error:
            raise ErrorPersistencia("No se pudo guardar el archivo de solicitudes") from error
        finally:
            if temporal is not None:
                temporal.unlink(missing_ok=True)
