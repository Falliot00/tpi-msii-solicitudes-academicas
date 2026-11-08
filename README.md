# Solicitudes académicas

Prototipo educativo para el TPI de Metodología de Sistemas II de:
- **Fermín Alliot** · Legajo 101414 · Comisión M25 C4-02
- **Gabriel Antuña** · Legajo 100506 · Comisión M25 C4-12
Carrera Tecnicatura Universitaria en Programación a Distancia. Datos operativos ficticios.

## Arquitectura y funcionalidades

El sistema permite registrar solicitudes, asignar responsables, cambiar estados,
consultar mediante filtros y generar reportes. El análisis distingue nueve
debilidades de la versión base y documenta cinco transformaciones de diseño.

| Módulo | Responsabilidad |
|---|---|
| `catalogos.py` | Estudiantes y responsables sintéticos compartidos |
| `dominio.py` | Solicitud, estados, tipos, prioridades e invariantes |
| `modulo.py` | Coordinación de las cinco operaciones del caso de uso |
| `repositorios.py` | Contrato de almacenamiento y adaptadores de memoria y JSON |
| `cli.py` | Interpretación de comandos, composición y presentación JSON |
| `inicial.py` | Versión base conservada para comparar diseño y comportamiento |

La consola selecciona el almacenamiento e inyecta su contrato en
`ModuloSolicitudes`. Las transiciones se resuelven en `Solicitud`; el dominio no
conoce rutas ni escritura en disco. Memoria y JSON satisfacen la misma interfaz
de tres operaciones: listar, obtener y guardar. El
[diagrama](docs/arquitectura.mmd) y las
[decisiones de diseño](docs/refactorings.md) detallan el alcance de SOLID.

## Instalación, ejecución y uso

Python 3.11 o superior. Sin dependencias para ejecutar el sistema y sus pruebas.
Clonar el repositorio y entrar en su carpeta:

```console
git clone https://github.com/Falliot00/tpi-msii-solicitudes-academicas.git
cd tpi-msii-solicitudes-academicas
```

```console
python -m solicitudes demo
python -m solicitudes --implementacion inicial demo
python -m solicitudes catalogos
python -m solicitudes --help
python -m unittest discover -s tests -v
```

Las demos utilizan memoria y no modifican archivos. Los demás comandos usan
datos/solicitudes.json o una ruta elegida con --archivo antes del comando.
Para repetir el ejemplo con ID 1, usar una ruta nueva:

```console
python -m solicitudes --archivo datos/ejemplo.json registrar --estudiante 1 --asunto "Constancia para beca" --detalle "Ciclo 2026" --tipo constancia --prioridad alta
python -m solicitudes --archivo datos/ejemplo.json asignar 1 1
python -m solicitudes --archivo datos/ejemplo.json estado 1 en_proceso
python -m solicitudes --archivo datos/ejemplo.json listar --estado en_proceso --prioridad alta --texto beca
python -m solicitudes --archivo datos/ejemplo.json estado 1 resuelta
python -m solicitudes --archivo datos/ejemplo.json reporte
```

Tomar el ID devuelto por registrar si ya existían datos. Para usar la versión
base con la consola actual, agregar --implementacion inicial antes del comando.
El tag estado-inicial conserva el ejecutable original, que se demostraba con
python -m solicitudes sin subcomando.

Abierta permite pasar a en_proceso (requiere responsable) o cancelada. En proceso
permite resuelta o cancelada. Los estados finales no admiten cambios ni
reasignación. Repetir un estado es idempotente. Los filtros se combinan con AND;
el texto busca parte del asunto sin distinguir mayúsculas ni eliminar tildes.
Salida JSON por stdout. Errores de dominio: código 2; de persistencia: código 3.
El archivo JSON no admite edición concurrente segura.

## Refactorings aplicados

| ID | Transformación | Diagnóstico | Comprobación asociada |
|---|---|---|---|
| R01 | Extract Method: validación con nombre de dominio | D01, D06 | Rechazo de registros inválidos en ambas versiones |
| R02 | Move Method: transiciones en Solicitud | D01, D05, D07 | Matriz de estados, responsable e idempotencia |
| R03 | Introduce Parameter Object: NuevaSolicitud y FiltroSolicitudes | D02 | Normalización y filtros combinados |
| R04 | Extract Class: repositorios por contrato inyectado | D04, D05 | Mismo contrato para memoria y JSON |
| R05 | Tipos de dominio, inmutabilidad y colección encapsulada | D03, D07, D08 | Inmutabilidad, copias y compatibilidad del archivo |

La protección ante archivo corrupto y el reemplazo atómico atienden D09 y se
registran como mejoras de robustez adicionales. Los fragmentos antes/después
están en [refactorings](docs/refactorings.md); la relación completa con pruebas
está en [trazabilidad](docs/trazabilidad.md). La nomenclatura se apoya en el
[catálogo de Fowler](https://refactoring.com/catalog/); los criterios de nombres,
funciones y comentarios se vinculan con
[Clean Code de Robert C. Martin](https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884).

## Validación

```console
python -m pip install -r requirements-dev.txt
python tools/verificar.py
```

El verificador conserva resultados de unittest, mypy estricto sobre la aplicación,
Ruff lint, formato, preservación de inicial.py y comparación de demos. Usa las
versiones fijadas en requirements-dev.txt. La suite contiene 40 métodos: los
mismos 13 casos para cada versión, tres de dominio, seis de repositorios y cinco
de consola. Los subcasos no se cuentan como tests independientes.

Validado con Windows y Python 3.14.6; Python 3.11 no se ejecutó por separado.
No se midió cobertura. No hay React/Next.js, por lo que React Doctor no corresponde.
Los resultados finales están en docs/evidencias/validacion.json.

## Historial y documentación

```console
git log --oneline --decorate
git tag --list
git diff estado-inicial estadorefactorizado -- solicitudes
git show estado-inicial:solicitudes/inicial.py
```

Tags: estado-inicial, estadorefactorizado, etapa-diagnostico, etapa-refactoring,
etapa-pruebas y etapa-docs. El nombre estadorefactorizado reproduce la consigna.
El archivo inicial permanece idéntico en la versión final.

- [Alcance y reglas](docs/alcance.md).
- [Diagnóstico de calidad y nueve debilidades](docs/diagnostico.md).
- [Checklist, revisión automatizada y revisión del autor](docs/code_review.md).
- [Informe técnico editable](docs/informe.md) y [guion de defensa](docs/guion_video.md).
- [Metodología y herramientas de asistencia](docs/ia/registro.md).
- [Referencias técnicas y aplicación al caso](docs/referencias_tecnicas.md).

Los resultados ejecutados se conservan en `docs/evidencias`.

El ZIP incluye Repositorio.bundle con commits y tags. Para recuperarlo desde
el ZIP extraído:

```console
git clone Repositorio.bundle solicitudes-academicas
```

La carpeta codigo del ZIP se puede ejecutar sin Git. El bundle conserva el
historial. El repositorio público está en:

https://github.com/Falliot00/tpi-msii-solicitudes-academicas

La publicación del código, documentación, commits y tags se realizó con
autorización explícita del estudiante.

## Informe y entrega

```console
python -m pip install -r requirements-documentacion.txt
python tools/construir_informe.py
python tools/empaquetar.py
```

El informe se guarda en entrega/Alliot_Fermin_TPI_MSII.pdf. Para empaquetar,
primero completar el cierre de Git. entrega/ está excluida del versionado para
evitar archivos recursivos y contenido dependiente de su propio commit.

Los enlaces del repositorio y del video de defensa están en config_entrega.json.
Video de defensa: https://youtu.be/wNdm-FbdRmc

## Autoría y herramientas de asistencia

Trabajo práctico grupal desarrollado por Fermín Alliot y Gabriel Antuña. Los integrantes
asumieron la autoría completa del diseño, arquitectura, programación del sistema base y
refactorizado, pruebas y revisión técnica. Se emplearon herramientas de IA exclusivamente
bajo el marco de la **Unidad 5 de la cátedra: "La IA como Copiloto"** (asistencia complementaria
en exploración sintáctica, datos sintéticos y soporte estilístico de redacción).

- [Anexo de metodología y herramientas de asistencia](docs/ia/registro.md).
- [Revisión técnica entre pares (Code Review)](docs/code_review.md).
- [Validación técnica local del equipo](docs/evidencias/validacion_manual.md).

Los datos de estudiantes y responsables son sintéticos.
