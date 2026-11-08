"""Operaciones del caso de uso. Recibe almacenamiento por su contrato."""

from typing import TypedDict

from solicitudes.dominio import Estado, FiltroSolicitudes, NuevaSolicitud, Solicitud, convertir_enum
from solicitudes.repositorios import RepositorioSolicitudes


class Reporte(TypedDict):
    total: int
    por_estado: dict[str, int]


class ModuloSolicitudes:
    """Coordinador de casos de uso para la gestión de solicitudes académicas.

    Aplica el principio de Inversión de Dependencias (DIP) interactuando
    exclusivamente con la abstracción RepositorioSolicitudes, manteniendo
    la lógica de negocio desacoplada de los detalles de almacenamiento.
    """

    def __init__(self, repositorio: RepositorioSolicitudes) -> None:
        self._repositorio = repositorio

    def registrar(self, nueva: NuevaSolicitud) -> Solicitud:
        nueva.validar()
        siguiente_id = max((s.id for s in self._repositorio.listar()), default=0) + 1
        solicitud = Solicitud(
            id=siguiente_id,
            estudiante_id=nueva.estudiante_id,
            asunto=nueva.asunto.strip(),
            detalle=nueva.detalle.strip(),
            tipo=nueva.tipo,
            prioridad=nueva.prioridad,
        )
        self._repositorio.guardar(solicitud)
        return solicitud

    def asignar(self, solicitud_id: int, responsable_id: int) -> Solicitud:
        solicitud = self._repositorio.obtener(solicitud_id).asignar(responsable_id)
        self._repositorio.guardar(solicitud)
        return solicitud

    def cambiar_estado(self, solicitud_id: int, estado: str) -> Solicitud:
        actual = self._repositorio.obtener(solicitud_id)
        solicitud = actual.cambiar_estado(convertir_enum(Estado, estado, "Estado inválido"))
        self._repositorio.guardar(solicitud)
        return solicitud

    def buscar(self, filtro: FiltroSolicitudes = FiltroSolicitudes()) -> list[Solicitud]:
        return [s for s in self._repositorio.listar() if filtro.coincide(s)]

    def reporte(self) -> Reporte:
        cantidades = {estado.value: 0 for estado in Estado}
        solicitudes = self._repositorio.listar()
        for solicitud in solicitudes:
            cantidades[solicitud.estado.value] += 1
        return {"total": len(solicitudes), "por_estado": cantidades}
