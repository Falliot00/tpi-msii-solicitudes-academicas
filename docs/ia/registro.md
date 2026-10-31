# Anexo de metodología y herramientas de asistencia

Herramienta: Codex de OpenAI en la aplicación de escritorio.
Fecha de trabajo: 31 de octubre de 2026, Argentina.
Grado de intervención: alto.

## Participación y alcance registrado

Fermín Alliot es el único integrante y responsable de la entrega y de su defensa.
Aportó los materiales de la cátedra, definió el alcance, seleccionó el caso de
solicitudes académicas y autorizó la publicación del repositorio.

La asistencia abarcó análisis de dominio y de calidad, identificación de
debilidades, alternativas de diseño, elaboración de las versiones inicial y
refactorizada, casos de prueba, ejecución de verificaciones, revisión técnica y
documentación. También comprendió los catálogos sintéticos y el formato del
informe. Su alcance registrado excede consultas de sintaxis o corrección de estilo.

## Síntesis de actividades y controles

Las cuatro filas agrupan actividades realizadas. Son resúmenes, no prompts
textuales ni un recuento de cuatro consultas aisladas. Los pedidos técnicos y
resultados de la revisión se conservan en [revision_agentes.md](revision_agentes.md).
Las respuestas personales del estudiante no se transcriben en este documento.

| ID | Actividad de asistencia | Evidencia y control realizado |
|---|---|---|
| A01 | Lectura de consigna y materiales; análisis del caso, diagnóstico y alternativas de diseño | Alcance, nueve debilidades, decisiones y trazabilidad contra el código inicial |
| A02 | Elaboración de ambas versiones, datos sintéticos y casos de prueba; ejecución de verificaciones | Historial Git, 13 pruebas iniciales, contrato compartido y suite final de 40 tests |
| A03 | Revisión de estándares y especificación mediante dos agentes de IA; correcciones y comprobación de hallazgos | Checklist, registro de revisión y prueba de invariantes; capturas documentales con fuentes |
| A04 | Redacción, estilo y organización del informe, README, guion y anexo; preparación y publicación autorizada | Markdown, PDF revisado visualmente, ZIP con hashes y repositorio público |

Los resultados de unittest, mypy y Ruff son ejecuciones de herramientas
orquestadas mediante la asistencia. La revisión por agentes es una comprobación
técnica automatizada. Ninguna de las dos acredita una validación manual personal
del estudiante o una aprobación docente.

## Criterio de validación humana posterior

Antes de defender el trabajo, corresponde contrastar las propuestas con la
consigna y el código, comprobar el antes/después, ejecutar los escenarios y
justificar los resultados. Una comprobación personal debe registrar fecha,
versión revisada, procedimiento, resultado y observaciones del estudiante.
Estos son criterios de revisión posterior; no se consignan como acciones
manuales ya ejecutadas sin un registro que las respalde.

En particular, la revisión debe explicar una transición rechazada, la función
de cada refactoring, la diferencia entre reorganización y robustez adicional,
y las limitaciones de JSON frente a concurrencia. La defensa requiere cámara
al inicio y voz propia. La grabación y su enlace permanecen pendientes.

## Conservación de evidencias

La consigna oficial, páginas 3 y 4, pide registrar intercambios relevantes y
declarar herramienta, finalidad y grado de intervención. Se mantienen los
pedidos de revisión, resultados y evidencias técnicas sin sustituirlos por
consultas no realizadas. Las versiones previas permanecen en el historial Git
y en el bundle del anexo. Los materiales originales de la cátedra no se modifican.
