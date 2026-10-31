"""Versión inicial educativa. Se conserva para comparar su diseño y comportamiento.

No proviene de un sistema de producción. Los problemas son diagnosticables
en este prototipo construido para el TPI, no incidentes atribuidos a usuarios.
"""

import json
from pathlib import Path
from typing import Any

from solicitudes.catalogos import ESTUDIANTES, RESPONSABLES


class GestorInicial:
    def __init__(self, archivo: Path | None = None) -> None:
        self.archivo = archivo
        self.datos: list[dict[str, Any]] = []
        if archivo is not None and archivo.exists():
            self.datos = json.loads(archivo.read_text(encoding="utf-8"))

    def procesar(
        self,
        accion: str,
        estudiante_id: int = 0,
        asunto: str = "",
        detalle: str = "",
        tipo: str = "",
        prioridad: str = "",
        solicitud_id: int = 0,
        responsable_id: int = 0,
        estado: str = "",
        texto: str = "",
    ) -> Any:
        if accion == "registrar":
            if estudiante_id not in [e.id for e in ESTUDIANTES]:
                raise ValueError("Estudiante inexistente")
            if not asunto.strip():
                raise ValueError("El asunto es obligatorio")
            if tipo not in ["constancia", "equivalencia", "inscripcion"]:
                raise ValueError("Tipo inválido")
            if prioridad not in ["baja", "media", "alta"]:
                raise ValueError("Prioridad inválida")
            s: dict[str, Any] | None = {
                "id": max([r["id"] for r in self.datos], default=0) + 1,
                "estudiante_id": estudiante_id,
                "asunto": asunto.strip(),
                "detalle": detalle.strip(),
                "tipo": tipo,
                "prioridad": prioridad,
                "estado": "abierta",
                "responsable_id": None,
            }
            self.datos.append(s)
            self._guardar()
            return s
        if accion == "asignar":
            s = None
            for r in self.datos:
                if r["id"] == solicitud_id:
                    s = r
                    break
            if s is None:
                raise ValueError("Solicitud inexistente")
            if responsable_id not in [r.id for r in RESPONSABLES]:
                raise ValueError("Responsable inexistente")
            if s["estado"] in ["resuelta", "cancelada"]:
                raise ValueError("Una solicitud cerrada no admite cambios")
            s["responsable_id"] = responsable_id
            self._guardar()
            return s
        if accion == "estado":
            s = None
            for r in self.datos:
                if r["id"] == solicitud_id:
                    s = r
                    break
            if s is None:
                raise ValueError("Solicitud inexistente")
            if estado not in ["abierta", "en_proceso", "resuelta", "cancelada"]:
                raise ValueError("Estado inválido")
            p = {
                "abierta": ["en_proceso", "cancelada"],
                "en_proceso": ["resuelta", "cancelada"],
                "resuelta": [],
                "cancelada": [],
            }
            if estado != s["estado"] and estado not in p[s["estado"]]:
                raise ValueError("Transición de estado no permitida")
            if estado == "en_proceso" and s["responsable_id"] is None:
                raise ValueError("Debe asignarse un responsable")
            s["estado"] = estado
            self._guardar()
            return s
        if accion == "listar":
            if estado and estado not in ["abierta", "en_proceso", "resuelta", "cancelada"]:
                raise ValueError("Estado inválido")
            if tipo and tipo not in ["constancia", "equivalencia", "inscripcion"]:
                raise ValueError("Tipo inválido")
            if prioridad and prioridad not in ["baja", "media", "alta"]:
                raise ValueError("Prioridad inválida")
            return [
                s
                for s in self.datos
                if (not estado or s["estado"] == estado)
                and (not tipo or s["tipo"] == tipo)
                and (not prioridad or s["prioridad"] == prioridad)
                and (not texto or texto.casefold() in s["asunto"].casefold())
            ]
        if accion == "reporte":
            return {
                "total": len(self.datos),
                "por_estado": {
                    e: sum(1 for s in self.datos if s["estado"] == e)
                    for e in ["abierta", "en_proceso", "resuelta", "cancelada"]
                },
            }
        raise ValueError("Acción desconocida")

    def _guardar(self) -> None:
        if self.archivo is not None:
            self.archivo.parent.mkdir(parents=True, exist_ok=True)
            self.archivo.write_text(
                json.dumps(self.datos, ensure_ascii=False, indent=2), encoding="utf-8"
            )
