"""Vocabulario e invariantes del dominio, sin dependencias de almacenamiento."""

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import TypedDict, TypeVar

from solicitudes.catalogos import ESTUDIANTES, RESPONSABLES


class TipoSolicitud(StrEnum):
    CONSTANCIA = "constancia"
    EQUIVALENCIA = "equivalencia"
    INSCRIPCION = "inscripcion"


class Prioridad(StrEnum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class Estado(StrEnum):
    ABIERTA = "abierta"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    CANCELADA = "cancelada"


TRANSICIONES = {
    Estado.ABIERTA: frozenset({Estado.EN_PROCESO, Estado.CANCELADA}),
    Estado.EN_PROCESO: frozenset({Estado.RESUELTA, Estado.CANCELADA}),
    Estado.RESUELTA: frozenset(),
    Estado.CANCELADA: frozenset(),
}

E = TypeVar("E", bound=StrEnum)


def convertir_enum(clase: type[E], valor: str, mensaje: str) -> E:
    try:
        return clase(valor)
    except ValueError:
        raise ValueError(mensaje) from None


@dataclass(frozen=True)
class NuevaSolicitud:
    estudiante_id: int
    asunto: str
    detalle: str
    tipo: TipoSolicitud
    prioridad: Prioridad

    def validar(self) -> None:
        validar_estudiante_y_asunto(self.estudiante_id, self.asunto)
        if not isinstance(self.tipo, TipoSolicitud):
            raise ValueError("Tipo inválido")
        if not isinstance(self.prioridad, Prioridad):
            raise ValueError("Prioridad inválida")

    @classmethod
    def desde_textos(
        cls, estudiante_id: int, asunto: str, detalle: str, tipo: str, prioridad: str
    ) -> "NuevaSolicitud":
        validar_estudiante_y_asunto(estudiante_id, asunto)
        return cls(
            estudiante_id,
            asunto,
            detalle,
            convertir_enum(TipoSolicitud, tipo, "Tipo inválido"),
            convertir_enum(Prioridad, prioridad, "Prioridad inválida"),
        )


def validar_estudiante_y_asunto(estudiante_id: int, asunto: str) -> None:
    if type(estudiante_id) is not int or estudiante_id not in {e.id for e in ESTUDIANTES}:
        raise ValueError("Estudiante inexistente")
    if not asunto.strip():
        raise ValueError("El asunto es obligatorio")


class RegistroSolicitud(TypedDict):
    id: int
    estudiante_id: int
    asunto: str
    detalle: str
    tipo: str
    prioridad: str
    estado: str
    responsable_id: int | None


@dataclass(frozen=True)
class Solicitud:
    id: int
    estudiante_id: int
    asunto: str
    detalle: str
    tipo: TipoSolicitud
    prioridad: Prioridad
    estado: Estado = Estado.ABIERTA
    responsable_id: int | None = None

    def __post_init__(self) -> None:
        if type(self.id) is not int or self.id <= 0:
            raise ValueError("Identificador inválido")
        NuevaSolicitud(
            self.estudiante_id, self.asunto, self.detalle, self.tipo, self.prioridad
        ).validar()
        if not isinstance(self.estado, Estado):
            raise ValueError("Estado inválido")
        if self.responsable_id is not None:
            if type(self.responsable_id) is not int or self.responsable_id not in {
                r.id for r in RESPONSABLES
            }:
                raise ValueError("Responsable inexistente")
        if self.estado in {Estado.EN_PROCESO, Estado.RESUELTA} and self.responsable_id is None:
            raise ValueError("Estado sin responsable")

    def asignar(self, responsable_id: int) -> "Solicitud":
        if responsable_id not in {r.id for r in RESPONSABLES}:
            raise ValueError("Responsable inexistente")
        if self.estado in {Estado.RESUELTA, Estado.CANCELADA}:
            raise ValueError("Una solicitud cerrada no admite cambios")
        return replace(self, responsable_id=responsable_id)

    def cambiar_estado(self, estado: Estado) -> "Solicitud":
        if estado != self.estado and estado not in TRANSICIONES[self.estado]:
            raise ValueError("Transición de estado no permitida")
        if estado == Estado.EN_PROCESO and self.responsable_id is None:
            raise ValueError("Debe asignarse un responsable")
        return replace(self, estado=estado)

    def a_registro(self) -> RegistroSolicitud:
        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "asunto": self.asunto,
            "detalle": self.detalle,
            "tipo": self.tipo.value,
            "prioridad": self.prioridad.value,
            "estado": self.estado.value,
            "responsable_id": self.responsable_id,
        }


@dataclass(frozen=True)
class FiltroSolicitudes:
    estado: Estado | None = None
    tipo: TipoSolicitud | None = None
    prioridad: Prioridad | None = None
    texto: str = ""

    def coincide(self, solicitud: Solicitud) -> bool:
        return (
            (self.estado is None or solicitud.estado == self.estado)
            and (self.tipo is None or solicitud.tipo == self.tipo)
            and (self.prioridad is None or solicitud.prioridad == self.prioridad)
            and (not self.texto or self.texto.casefold() in solicitud.asunto.casefold())
        )
