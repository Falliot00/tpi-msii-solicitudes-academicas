"""Catálogos sintéticos compartidos por las dos versiones."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Estudiante:
    id: int
    nombre: str


@dataclass(frozen=True)
class Responsable:
    id: int
    nombre: str
    area: str


ESTUDIANTES = (Estudiante(1, "Estudiante Alfa"), Estudiante(2, "Estudiante Beta"))
RESPONSABLES = (
    Responsable(1, "Responsable Uno", "Alumnado"),
    Responsable(2, "Responsable Dos", "Coordinación"),
)
