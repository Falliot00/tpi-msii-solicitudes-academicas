# Registro de uso de inteligencia artificial

Herramienta: Codex de OpenAI en la aplicación de escritorio.
Fecha de trabajo: 31 de octubre de 2026, Argentina.
Grado de intervención: alto.

Fermin Alliot es el único integrante. Aportó los materiales de la materia,
definió el alcance de la entrega, seleccionó el caso de solicitudes académicas
y autorizó su publicación. La IA generó las versiones inicial y refactorizada,
las pruebas y la documentación, y ejecutó comprobaciones y revisión técnica.
La revisión personal del material y la defensa con voz propia quedan a cargo
del estudiante.

## Registro resumido de actividades

El registro conserva objetivos, decisiones y resultados sin transcribir las
preguntas o respuestas personales del estudiante. Los pedidos técnicos de
revisión y sus resultados permanecen en revision_agentes.md.

### I01 Material de referencia

Se consultaron la consigna TP MS2V2.pdf, los modelos de presentación y materiales
de las unidades 1, 3 y 4. La consigna oficial se tomó como referencia normativa.

### I02 Alcance y caso seleccionado

Se definió una entrega con sistema base y refactorizado, informe, anexo y guion
para el video. Se eligió el caso de solicitudes académicas y la modalidad
individual. El prototipo utiliza catálogos ficticios, cinco operaciones y
almacenamiento en memoria o JSON.

### I03 Construcción y diagnóstico

Se construyó GestorInicial y se ejecutaron 13 pruebas de caracterización antes
del refactoring. Se conservó el tag estado-inicial, se documentaron nueve
debilidades y se reorganizó el código en dominio, módulo, repositorios y consola.
Evidencias: commits, diagnostico.md, refactorings.md y pruebas_iniciales.txt.

### I04 Verificación y revisión

Se ejecutaron unittest, mypy y Ruff, se compararon las demos y se aplicó una
revisión por estándares y por especificación mediante dos agentes de IA.
Los hallazgos y sus correcciones están registrados en code_review.md y
revision_agentes.md. La validación final incluye 40 tests y resultados
conservados en docs/evidencias.

### I05 Documentación y entrega

Se redactaron el informe, las decisiones de diseño, las conclusiones y el guion.
Se generaron el PDF y el ZIP con código, historial y evidencias. El guion prepara
la exposición; la grabación con cámara inicial y voz propia está pendiente.

### I06 Publicación

Con autorización del estudiante se creó el repositorio público y se publicaron
main y los seis tags. Se incorporó el enlace real al informe y al anexo:
https://github.com/Falliot00/tpi-msii-solicitudes-academicas

## Revisión de las propuestas

Las decisiones se relacionan con problemas observados y con comprobaciones
ejecutadas. Las limitaciones y las mejoras futuras se distinguen de resultados
ya verificados. La declaración de uso de IA corresponde a las tareas realizadas
y no sustituye la responsabilidad individual sobre la entrega y su defensa.
