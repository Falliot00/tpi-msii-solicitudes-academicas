# Registro de la revisión técnica por dos ejes

Herramienta: skill code-review de Matt Pocock, ejecutada con dos agentes de IA.
No participaron revisores humanos. Base completa verificada: commit raíz vacío
5dbf7891722b167b0a6ed859e018de05fd89c0f1. Primer HEAD revisado: 6ccaa11.
Comando de revisión: git diff 5dbf789...HEAD. Status limpio. La revisión abarcó
43 archivos y 3009 líneas nuevas, no un diff vacío ni solo el último commit.
Commits revisados: 4680f99, 9428229, b72be77, 0ed754f, 3b5e37b y 6ccaa11.

## Pedido enviado al eje Standards

Transcripción del contenido técnico del pedido, con la ruta local del
repositorio abreviada como RAÍZ y sin cambiar sus criterios:

"Aplicá el eje Standards de la skill code-review, SOLO LECTURA, sin editar ni
ejecutar toda la suite. Repo: RAÍZ. Base verificada raíz vacía
5dbf7891722b167b0a6ed859e018de05fd89c0f1; HEAD 6ccaa11. Diff obligatorio completo:
git diff 5dbf789...HEAD; lista de commits: 4680f99 feat base, 9428229 fix tipos,
b72be77 diagnóstico, 0ed754f refactor, 3b5e37b verificación, 6ccaa11 docs.
Incluir status y nuevos/staged/unstaged si los hubiera; confirmar diff no vacío.
Fuentes de estándares: pyproject.toml, README.md, docs/alcance.md,
docs/refactorings.md, AGENTS del proyecto padre (archivos sources solo lectura;
no ampliar alcance; validaciones apropiadas; preservar ajenos; commits atómicos,
sin push). La versión solicitudes/inicial.py debe preservarse idéntica al tag
estado-inicial, con los defectos pedagógicos diagnosticados; no pedir su
refactor ni omitir checks. Final app en Python estándar, tipos estrictos, sin
React. Ya se ejecutaron 39 tests, mypy y Ruff PASS. Revisá fallos reales, límites
de contratos y robustez; no reportes cuestiones impuestas por herramientas.
Baseline de smells obligatorio (heurísticas, no infracciones duras): Mysterious
Name nombre que no revela intención -> renombrar; Duplicated Code misma lógica
repetida -> extraer; Feature Envy usa datos de otro -> mover; Data Clumps campos
que viajan juntos -> agrupar; Primitive Obsession primitivos para concepto de
dominio -> tipo propio; Repeated Switches cascadas por mismo tipo -> polimorfismo
o mapa único; Shotgun Surgery cambio lógico disperso -> reunir; Divergent Change
módulo cambia por razones distintas -> separar; Speculative Generality
abstracciones hipotéticas -> quitar; Message Chains navegación larga -> ocultarla;
Middle Man solo delega -> eliminar; Refused Bequest ignora herencia -> composición.
Regla documentada del repo prevalece; cada smell es juicio. Reportar por
archivo/línea (a) infracciones de estándar documentado con fuente y regla,
(b) smells posibles con evidencia y distinción de juicio. Menos de 400 palabras,
en español. Si hay bug, indicá reproducción concreta y prioridad. No crear
archivos ni commits."

## Standards

Resultado original, conservado en forma ligeramente abreviada:

"Infracción documentada [P2]: entidades inválidas pueden inutilizar el
repositorio JSON. Solicitud permite construir valores que vulneran invariantes;
guardar los escribe sin validarlos. Contradice que el dominio concentra
invariantes y que los adaptadores son sustituibles. Construir
Solicitud(1, 99, 'Constancia', '', TipoSolicitud.CONSTANCIA, Prioridad.MEDIA)
y guardarla hace que Memoria la recupere pero JSON rechace la siguiente lectura.
También ocurre con ID cero o resuelta sin responsable. Todos los argumentos
cumplen las anotaciones. Posible Duplicated Code: la validación de estudiante
se repite en dominio y deserializador. Centralizarla reduciría diferencias."

Acción: Solicitud.__post_init__ valida invariantes antes de persistir; JSON
valida formato y delega las reglas a la entidad. Se agregó una prueba de
construcción con diez subcasos inválidos, incluidos booleanos como IDs.

Pedido de seguimiento: "Verificá SOLO el cierre de tu hallazgo y el delta nuevo
(no repetir fase completa ni suite). HEAD ahora 52d3d6f; git diff 6ccaa11..HEAD
muestra correcciones. [...] Confirmá si queda cerrado P2 y smell asociado, y
si el delta introduce un defecto nuevo. [...] No editar."
Los puntos suspensivos identifican detalles de implementación resumidos;
el resultado y el alcance se conservan aquí sin atribuir una revisión adicional.

Respuesta final del revisor:

"P2 cerrado. Solicitud.__post_init__ rechaza las entidades inválidas antes de
que lleguen a cualquier repositorio. Reejecuté únicamente la reproducción
original: ahora lanza ValueError durante la construcción; una entidad válida
conserva correctamente su ida y vuelta por serialización. Smell asociado
cerrado. _desde_registro delega las invariantes en Solicitud y conserva las
comprobaciones de formato, eliminando la duplicación señalada. Revisé el delta
6ccaa11..52d3d6f, incluidas herramientas y modificaciones documentales: no detecté
nuevos defectos accionables. Los registros conservan PASS de 40 tests, mypy,
Ruff y formato; no repetí esas validaciones. Git continúa limpio. No edité archivos."

## Pedido enviado al eje Spec

Se transcribe el contenido técnico con RAÍZ como abreviatura de la ruta local:

"Aplicá eje Spec de skill code-review SOLO LECTURA. No editar ni repetir suite
completa. Repo RAÍZ. Base verificada 5dbf7891722b167b0a6ed859e018de05fd89c0f1
(raíz vacía), HEAD 6ccaa11. Diff obligatorio: git diff 5dbf789...HEAD; commits
4680f99,9428229,b72be77,0ed754f,3b5e37b,6ccaa11. Incluir status y cambios
staged/unstaged/nuevos si existen. Especificación: docs/alcance.md y consigna
oficial TP MS2V2.pdf (6 páginas). Pedido usuario: TPI completo sistema
base/refactorizado, informe, anexo y guion; caso solicitudes académicas; único
integrante Fermin Alliot 101414 comisión M25 C4-02. No pide PPTX ni grabar voces;
Git push/publicación no autorizados. GitHub/video declarados pendientes, config
URLs null, se preparan localmente. PDF generado en entrega/Alliot_Fermin_TPI_MSII.pdf;
ZIP se empaquetará al cerrar revisión; tags etapa-docs y estadorefactorizado
se fijarán tras cierre, los otros ya existen. No reportar estos pasos programados
como defectos implementativos, pero sí cualquier afirmación falsa de cumplimiento.
Consigna: ≥3 entidades, ≥4 operaciones, persistencia/memoria, ≥8 debilidades con
evidencia/ubicación/impacto/riesgo/prioridad, SOLID según corresponda, ≥4 refactors
incluyendo Extract Method, Move Method/reubicación, Parameter Object/equivalente;
pruebas antes/después, review checklist aplicado, PDF resumen 5-7 líneas,
prompts relevantes y declaración IA, README/docs/historial/tags específicos,
guion 10-15 minutos voz propia cámara inicial. Modelo solo orientativo.
Reportá (a) requisitos faltantes/parciales, (b) ampliaciones ajenas,
(c) requisitos implementados erróneamente, citando frase exacta del requisito
y archivo/línea. Menos de 400 palabras en español; distinguir limitaciones
externas conocidas y errores nuevos. No crear archivos ni commits."

## Spec

Resultado original: un hallazgo documental P2, incorporar capturas de evidencias.
La consigna pide desarrollo respaldado con capturas, tablas y fragmentos de
código. El PDF tenía tablas, código y un diagrama, pero carecía de capturas.
No se detectaron ampliaciones ajenas ni defectos funcionales respecto del alcance.

Acción: incorporar dos capturas tomadas del navegador sobre un panel documental
local alimentado por los logs ejecutados, con fuentes explícitas y aclaración
de que no representa una GUI del producto. No se inventaron pantallas operativas.

Pedido de seguimiento: "Verificá SOLO cierre del hallazgo documental y delta,
sin repetir suite ni revisión completa. HEAD52d3d6f. Imágenes reales del navegador
sobre panel documental local: docs/evidencias/captura_demo.jpg,
captura_validacion.jpg y captura_panel.jpg; logs fuentes conservados. PDF
regenerado en entrega/Alliot_Fermin_TPI_MSII.pdf incorpora capturas y explica
que es una visualización de logs, no GUI de producto. [...] Confirmá que se
cerró falta de capturas y si hubo defecto nuevo del delta. [...] No editar."

Respuesta final del revisor:

"Hallazgo cerrado. En HEAD 52d3d6f, el PDF incorpora dos capturas legibles en
las páginas 13 y 14: comparación de demos y validación. Ambas identifican sus
archivos fuente; el informe aclara que muestran un panel documental de logs
y que el producto funciona por consola. Revisé el delta desde 6ccaa11, incluida
la centralización de invariantes en Solicitud.__post_init__, su reutilización
al cargar JSON y la prueba añadida. No detecté defectos nuevos de especificación
en ese delta. Git está limpio. No modifiqué archivos ni repetí la suite. Los
40 tests PASS constan en las evidencias existentes; no representan una ejecución
mía. Enlaces externos, tags finales y ZIP continúan como pasos de cierre conocidos."

## Cierre y límites

Standards: una infracción P2 y un posible smell asociado, ambos cerrados.
Spec: un hallazgo documental P2, cerrado. Ningún hallazgo técnico pendiente
detectado en el alcance revisado. La revisión no demuestra ausencia de todos
los bugs y no incluye aprobación humana. La grabación del video y la publicación
GitHub requieren completar acciones externas reales.
