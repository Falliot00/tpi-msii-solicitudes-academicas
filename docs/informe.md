# Resumen ejecutivo

Se analizó un prototipo local de gestión de solicitudes académicas.
El sistema inicial funciona en los casos comprobados y reúne nueve debilidades.
Se aplicaron cinco transformaciones de diseño vinculadas a SOLID y Clean Code.
Las pruebas comparan ambas versiones y verifican reglas, errores y persistencia.
El resultado conserva las operaciones y mejora el aislamiento de responsabilidades.
Su uso se limita a un entorno educativo local con datos ficticios y sin concurrencia.

## Propósito del trabajo

El trabajo integra diagnóstico de calidad, deuda técnica, refactoring seguro y
revisión de código sobre un caso acotado. El criterio de éxito es mostrar qué
cambió internamente, por qué se eligió esa transformación y qué evidencia
permite confiar en el comportamiento. Se priorizó la trazabilidad del proceso.

La consigna TP MS2V2.pdf constituye la referencia normativa. La presentación
PowerPoint, la guía rápida y su README se emplearon como orientación para el
orden de exposición. El sistema TurnoPlus del modelo es un ejemplo ajeno a este
caso y no se presenta como un trabajo realizado.

## Identificación y modalidad

Único integrante: Fermin Alliot. Legajo: 101414. Comisión: M25 C4-02.
Carrera: Tecnicatura Universitaria en Programación a Distancia.
Materia: Metodología de Sistemas 2. Fecha de elaboración: 31 de octubre de 2026.

Se construyó un prototipo para la actividad con asistencia de IA. Se conserva
la versión inicial ejecutada y el historial real de las mejoras. No se afirma
que el sistema provenga de producción ni que haya tenido usuarios reales.

<!-- salto -->
# 1 Sistema base y alcance

El caso es un sistema de gestión de solicitudes académicas. Un operador registra
pedidos de estudiantes y los deriva a responsables de Alumnado o Coordinación.
El estudiante es el origen de la solicitud; el operador ejecuta los comandos;
el responsable atiende el caso. Estos son roles del modelo, sin autenticación
ni cuentas separadas en el prototipo.

| Estructura | Datos principales | Representación inicial y final |
|---|---|---|
| Estudiante | ID y nombre ficticio | Dataclass inmutable en ambas versiones |
| Responsable | ID, nombre ficticio y área | Dataclass inmutable en ambas versiones |
| Solicitud | ID, estudiante, asunto, detalle, tipo, prioridad, estado y responsable | Diccionario inicial; dataclass inmutable en la versión final |

## Funcionalidades verificables

1. Registrar solicitudes de constancia, equivalencia o inscripción con prioridad baja, media o alta.
2. Asignar y reasignar responsables existentes mientras la solicitud no esté cerrada.
3. Cambiar estado respetando transiciones y exigir responsable para comenzar la atención.
4. Buscar por estado, tipo, prioridad y texto parcial del asunto con filtros combinados.
5. Generar un reporte total y por estado, incluyendo estados sin solicitudes.

Se supera el mínimo de tres estructuras y cuatro operaciones de la consigna.
Los catálogos contienen dos estudiantes y dos responsables ficticios. No se usa
el nombre del autor como dato operativo de un estudiante del sistema.

## Tecnología y límites

Python 3.11 o superior, biblioteca estándar, consola y JSON local. Se eligió una
tecnología que permite expresar objetos, enums y contratos sin infraestructura
externa. Las reglas no dependen de un framework. Se usa unittest para pruebas,
mypy para tipos y Ruff para lint y formato. La ejecución no requiere instalar
dependencias; las herramientas de desarrollo sí se instalan por separado.

Quedan fuera del alcance: interfaz web, autenticación, autorización, correo,
adjuntos, gestión de catálogos y edición concurrente. No se invoca React Doctor
porque no se modificó React ni Next.js.

<!-- salto -->
# 2 Reglas y evidencia de funcionamiento

El estado inicial tiene el tag estado-inicial, commit 9428229. Su método
GestorInicial.procesar implementa las cinco operaciones y persiste en memoria
o archivo. Sus 13 pruebas se ejecutaron antes de iniciar la reorganización.
La salida original está en docs/evidencias/pruebas_iniciales.txt.

## Reglas observables

Un alta requiere estudiante existente, asunto no vacío, tipo y prioridad
válidos. Asunto y detalle pierden espacios exteriores. Los identificadores
son enteros correlativos calculados a partir de los existentes. La búsqueda
por asunto usa casefold y no elimina tildes. Los filtros se combinan con AND.

| Estado actual | Siguiente estado permitido | Condición |
|---|---|---|
| abierta | en_proceso o cancelada | en_proceso requiere responsable |
| en_proceso | resuelta o cancelada | Ya existe responsable |
| resuelta | Ningún estado diferente | No permite reasignar |
| cancelada | Ningún estado diferente | No permite reasignar |

Repetir el mismo estado es idempotente. No se permite saltar directamente de
abierta a resuelta ni reabrir una solicitud cerrada. No hay eliminación de casos.

## Evidencia E01 de la demo inicial

La ejecución original registra una constancia, asigna al responsable 1 y pasa a
en_proceso. Este extracto procede de la salida ejecutada, no de una captura de
una interfaz inexistente:

```json
{
  "id": 1,
  "estudiante_id": 1,
  "asunto": "Certificado regular",
  "estado": "en_proceso",
  "responsable_id": 1
}
```

El reporte indica total 1, en_proceso 1 y cero en los otros estados. La salida
completa, con el detalle y la prioridad, está en demo_inicial.txt. La demo final
también conserva una instantánea de cada paso para comparar ambas versiones.

<!-- salto -->
# 3 Calidad externa e interna

## Calidad externa comprobada

En los escenarios probados, el operador puede dar de alta una solicitud,
asignarla, cambiar su estado y consultar información coherente. Los datos
inválidos se rechazan con mensajes. La recuperación desde JSON permite continuar
entre ejecuciones. Estas observaciones corresponden a pruebas de software y a
la demo local; no equivalen a una evaluación de satisfacción o usabilidad.

## Calidad interna observada

El mismo flujo decide cinco acciones y recibe diez argumentos además de self.
Las búsquedas de solicitudes se repiten, los estados aparecen como cadenas
dispersas y la escritura de archivos comparte clase con las reglas. El código
puede funcionar en los ejemplos y exigir demasiado cuidado para modificarse.

| Cambio futuro concreto | Dificultad inicial | Localización después del cambio |
|---|---|---|
| Sustituir memoria por JSON | La clase gestora conoce rutas y escritura | Se selecciona un adaptador de repositorio |
| Revisar una transición | Hay que navegar el método general | Solicitud.cambiar_estado y TRANSICIONES |
| Agregar un filtro | Más parámetros al flujo genérico | FiltroSolicitudes y su criterio |
| Proteger datos devueltos | Diccionarios públicos compartidos | Entidad inmutable y registro independiente |

## Deuda técnica y prioridad

La deuda técnica se expresa como costo y riesgo de cambios futuros. En este
prototipo no se midieron horas perdidas, incidentes ni impacto económico. La
priorización es cualitativa: primero proteger invariantes y datos, luego reducir
repetición y ambigüedad. Las siguientes páginas identifican nueve debilidades
con evidencia y ubicación estable en el archivo inicial.

Un smell es una señal que requiere juicio. No se presenta toda función larga
como defectuosa por su tamaño ni se denomina God Class a este prototipo pequeño.
El diagnóstico se apoya en responsabilidades y conocimiento duplicado.

<!-- salto -->
# 4 Diagnóstico de deuda técnica

## D01 Long Method

**Evidencia y ubicación:** inicial.py, procesar, líneas 22 a 116. Una misma
operación decide registro, asignación, transición, consulta y reporte.
**Impacto:** leer o corregir una acción requiere recorrer lógica ajena.
**Riesgo:** introducir una regresión al modificar una rama. **Prioridad:** alta.
**Tratamiento:** operaciones separadas y extracción de validación, R01 y R02.

## D02 Long Parameter List

**Evidencia y ubicación:** firma de procesar, líneas 22 a 34, diez argumentos
además de self. Cada acción utiliza solo un subconjunto. **Impacto:** llamadas
con datos irrelevantes y combinaciones ambiguas. **Riesgo:** confundir parámetros.
**Prioridad:** media. **Tratamiento:** NuevaSolicitud y FiltroSolicitudes, R03.

## D03 Primitive Obsession

**Evidencia y ubicación:** diccionario de registro y validaciones de literales,
líneas 39 a 51 y 80 a 86. **Impacto:** el vocabulario del dominio no se concentra
en tipos explícitos. **Riesgo:** errores de escritura o valores no previstos en
cambios futuros. **Prioridad:** alta. **Tratamiento:** enums y Solicitud, R05.

## D04 Duplicated Code

**Evidencia y ubicación:** bucles de búsqueda de las ramas asignar y estado,
líneas 57 a 64 y 72 a 79. **Impacto:** la misma corrección debe repetirse.
**Riesgo:** distinto manejo de un ID ausente. **Prioridad:** media.
**Tratamiento:** Repositorio.obtener, R04.

Las cuatro debilidades están respaldadas por código concreto. No se afirma
que las pruebas iniciales fallen por ellas; el objetivo es reducir el costo de
mantener una funcionalidad que ya se encuentra comprobada.

<!-- salto -->
# 4 Diagnóstico de deuda técnica continuación

## D05 Responsabilidades divergentes

**Evidencia y ubicación:** GestorInicial.procesar y _guardar. Validación,
reglas, consultas y escritura JSON conviven. **Impacto:** cambia la misma clase
por decisiones independientes. **Riesgo:** acoplamiento de persistencia y negocio.
**Prioridad:** alta. **Tratamiento:** extraer repositorio e inyectarlo, R04.

## D06 Nombres poco expresivos

**Evidencia y ubicación:** variables s, r y p en búsquedas y transiciones.
**Impacto:** el significado depende del contexto de cada rama. **Riesgo:**
errores durante lectura y revisión. **Prioridad:** media. **Tratamiento:**
operaciones y nombres del dominio, R01 y R02.

## D07 Estado mutable expuesto

**Evidencia y ubicación:** self.datos público y retorno de nueva, s y listar.
**Impacto:** un consumidor Python puede modificar el dato almacenado sin pasar
por las reglas. **Riesgo:** romper invariantes. **Prioridad:** alta.
**Tratamiento:** entidad frozen y colecciones independientes, R05.

## D08 Conocimiento duplicado de catálogos

**Evidencia y ubicación:** literales repetidos en registro, transición,
filtros y reporte, líneas 39 a 42, 80 a 100 y 113. **Impacto:** agregar un valor
obliga a revisar varias ramas. **Riesgo:** omitirlo en una validación o reporte.
**Prioridad:** media. **Tratamiento:** vocabulario central en enums, R05.

## D09 Escritura directa del archivo

**Evidencia y ubicación:** _guardar, líneas 118 a 124, write_text sobre el destino.
**Impacto:** una interrupción podría truncarlo. **Riesgo:** pérdida de datos locales.
**Prioridad:** alta. **Tratamiento:** temporal y reemplazo atómico. Es una mejora
de robustez, no se contabiliza como refactoring puro.

<!-- salto -->
# 5 Diseño final y principios aplicados

La versión final distribuye las responsabilidades en cuatro lugares: dominio,
módulo de casos de uso, repositorios y consola. El módulo ofrece registrar,
asignar, cambiar_estado, buscar y reporte. El contrato de almacenamiento tiene
listar, obtener y guardar. Se evita introducir interfaces para dependencias
que todavía no existen.

<!-- arquitectura -->

| Principio | Evidencia concreta y límite |
|---|---|
| SRP | Solicitud protege transiciones; ModuloSolicitudes coordina; repositorios almacenan; CLI presenta |
| OCP | Elegir memoria o JSON no cambia las reglas. Agregar un estado sí exige revisar reglas y pruebas |
| LSP | Ambos adaptadores satisfacen un contrato común de almacenamiento y error de ausencia; JSON puede presentar fallos de I/O documentados |
| ISP | Tres operaciones usadas por el módulo; no se exige a implementaciones cumplir funciones ajenas |
| DIP | El constructor recibe RepositorioSolicitudes, definido como Protocol, en lugar de crear RepositorioJson |

Clean Code se aplica mediante nombres expresivos, funciones enfocadas, objetos
de parámetros y errores comprensibles. La entidad es inmutable y devuelve un
nuevo valor al cambiar. La conversión a JSON produce un diccionario independiente.
La CLI separa errores de dominio (código 2) y persistencia (código 3).

<!-- salto -->
# 6 Refactorings con evidencia antes y después

## R01 Extract Method

Antes, el alta incluía dentro del método general:

```python
if estudiante_id not in [e.id for e in ESTUDIANTES]:
    raise ValueError("Estudiante inexistente")
if not asunto.strip():
    raise ValueError("El asunto es obligatorio")
```

Después, validar_estudiante_y_asunto expresa la regla y NuevaSolicitud la utiliza.
La conversión desde texto preserva la precedencia de errores. Atiende D01 y D06.
Prueba asociada: test_registros_invalidos_no_se_guardan en ambas versiones.

## R02 Move Method y reubicación de responsabilidad

Antes, procesar leía s["estado"], creaba el mapa p y mutaba el diccionario.
Después, Solicitud.cambiar_estado protege la transición; el módulo coordina:

```python
actual = self._repositorio.obtener(solicitud_id)
solicitud = actual.cambiar_estado(
    convertir_enum(Estado, estado, "Estado inválido")
)
self._repositorio.guardar(solicitud)
```

La regla queda junto al estado al que protege. No cambia el recorrido permitido.
Atienden D01, D05 y D07. Pruebas asociadas: matriz de 16 pares, responsable
obligatorio, saltos, reapertura e idempotencia.

Las ubicaciones completas y el razonamiento están en docs/refactorings.md.
La evidencia de antes se vincula al tag estado-inicial y la de después al
tag estadorefactorizado. No se reemplaza la versión inicial por una simulación
reconstruida al final del proceso.

<!-- salto -->
# 6 Refactorings continuación

## R03 Introduce Parameter Object

Antes, procesar recibía diez argumentos de operaciones diferentes. Después,
registrar recibe NuevaSolicitud y buscar recibe FiltroSolicitudes. Se agrupan
datos que viajan juntos y desaparecen parámetros sin sentido para la acción.

```python
def registrar(self, nueva: NuevaSolicitud) -> Solicitud:
    nueva.validar()
```

Atiende D02. Lo verifican registro normalizado y filtros combinados.

## R04 Extract Class e inversión de dependencia

Antes, GestorInicial escribía el archivo y repetía la búsqueda por ID. Después,
RepositorioMemoria y RepositorioJson cumplen listar, obtener y guardar. El
módulo recibe ese contrato. La CLI selecciona el adaptador sin modificar reglas.
Atienden D04 y D05. El mismo contrato de prueba se aplica a ambos almacenamientos.

## R05 Reemplazar primitivas y encapsular colección

Antes, las solicitudes eran diccionarios mutables con cadenas dispersas.
Después, Estado, TipoSolicitud y Prioridad definen vocabulario; Solicitud es
inmutable. La lista devuelta puede modificarse sin afectar el repositorio.
Atienden D03, D07 y D08. Se verifica inmutabilidad y compatibilidad del JSON.

## Mejoras adicionales de robustez

El adaptador JSON valida estructura, identificadores, referencias y estados.
Para escribir, genera un temporal en la misma carpeta y utiliza os.replace.
Un archivo corrupto se rechaza sin sobrescribirlo. Un fallo de reemplazo debe
preservar el destino y limpiar el temporal. Estas mejoras amplían garantías
ante fallos y tienen pruebas propias; no se presentan como reorganización pura.

<!-- salto -->
# 7 Pruebas y verificación

Primero se ejecutaron 13 pruebas de caracterización sobre la versión inicial.
Después se aplicaron los mismos escenarios y expectativas a la versión final.
La estructura de las pruebas separa preparación, acción y verificación. Los
casos de éxito se complementan con errores, bordes y persistencia.

| Grupo | Qué verifica | Cantidad de tests |
|---|---|---|
| Contrato inicial | Alta, IDs, validaciones, estados, filtros, reporte y archivo | 13 |
| Mismo contrato final | Mismas expectativas observables | 13 |
| Dominio | Matriz, inmutabilidad e invariantes de construcción | 3 |
| Repositorios | Contrato común, acentos, formatos inválidos y fallo de reemplazo | 6 |
| Consola e integración | Demos, compatibilidad JSON, errores y precedencia | 5 |
| Total | Suite completa | 40 |

Los subcasos de la matriz y los formatos inválidos se ejecutan con subTest;
no se suman como métodos de prueba independientes para inflar la cantidad.

## Estrategia de comparación

El contrato compartido compara contra valores esperados, no solo contra otra
implementación que podría compartir el mismo error. Además, las demos de ambas
versiones deben producir JSON idéntico. Una prueba carga con la versión final
un archivo escrito por la inicial, sin exigir migración manual.

## Incidencia encontrada durante la verificación

La primera comparación de demos falló porque el estado inicial devolvía
referencias mutables. El agregador de la demostración conservaba esas referencias
y los cambios posteriores alteraban los resultados previos. Se corrigió la
captura con deepcopy por paso, sin cambiar las reglas iniciales ni debilitar
el test. El fallo original está en incidencia_demo_mutable.txt y la revisión
lo registra como CR01. La reejecución mínima de ese test pasó.

<!-- salto -->
# 7 Resultados de validación

<!-- validacion -->

## Evidencias incluidas

- E01: ejecución original de la demo y las 13 pruebas previas al refactoring.
- E02: suite completa y comparación de demos de ambas implementaciones.
- E03: typecheck de los ocho módulos Python de la aplicación.
- E04: lint y comprobación de formato del código del repositorio.
- E05: diff que comprueba que inicial.py conserva el contenido del tag base.
- E06: archivo del fallo real de la demo y registro de su corrección.

Las salidas completas se conservan en docs/evidencias. Se incluyen comandos,
códigos de salida y fecha con zona horaria en validacion.json. La cantidad de
tests y los resultados corresponden a ejecución real. No se informa cobertura
porque no se midió; tampoco se afirma haber probado múltiples sistemas operativos.

## Limitaciones de la verificación

La ejecución se realizó con Python 3.12 en Windows. El código declara Python
3.11 como mínimo, pero esa versión no se ejecutó por separado. No se hicieron
pruebas de carga, penetración, múltiples procesos ni durabilidad ante corte de
energía. El manejo de un fallo de reemplazo se probó mediante OSError simulado.
Las pruebas de consola no equivalen a validación con usuarios académicos reales.

Typecheck y lint detectan determinadas clases de errores; no sustituyen los
tests ni la defensa. El archivo inicial mantiene tipos dinámicos explícitos
porque es parte del caso diagnosticado; mypy también lo verifica sin omitirlo.

<!-- salto -->
# 7 Capturas de las evidencias ejecutadas

Las imágenes siguientes son capturas del panel documental local que presenta
salidas registradas por las herramientas. No representan una interfaz gráfica
del producto: el sistema se usa mediante consola. Los datos completos originales
se conservan en los archivos identificados debajo de cada captura.

<!-- captura_demo -->

E07. Comparación del resultado de listar en las demos inicial y refactorizada.
Fuente: demo_inicial.json y demo_refactorizada.json. Se conserva ID, estado,
responsable y demás campos observables.

<!-- salto -->
# 7 Captura de validación

<!-- captura_validacion -->

E08. Resultados del verificador y resumen real de la suite. Fuente:
validacion.json y suite_completa.txt. Las capturas se tomaron del panel local
después de ejecutar las comprobaciones; no se dibujaron valores de PASS sin respaldo.

<!-- salto -->
# 8 Code review profesional

La revisión utiliza un checklist de funcionalidad, diseño, legibilidad, errores,
datos, persistencia, pruebas y documentación. Se redacta feedback sobre el código
y sus efectos. La revisión está asistida por IA y se distingue de una revisión
humana o una aprobación docente.

| Observación | Acción correctiva y aceptación |
|---|---|
| CR01 Resultados de demo compartían referencias mutables | Capturas independientes; igualdad de ambas demos |
| CR02 Anotaciones locales incompatibles | Tipos precisados antes de fijar el estado inicial validado |
| CR03 Riesgo de escritura directa | Temporal y reemplazo; destino intacto ante fallo simulado |
| CR04 JSON inválido podía afectar la operación | Rechazo controlado sin sobrescritura |
| CR05 Construcción directa permitía una entidad inválida | Invariantes en __post_init__; rechazo antes de persistir y prueba específica |

## Criterios de aceptación técnica

1. Conservar resultados y rechazos acordados de las cinco operaciones.
2. Impedir transiciones prohibidas y modificaciones de solicitudes cerradas.
3. Mantener invariantes a través de una entidad inmutable y almacenamiento por contrato.
4. Pasar suite, typecheck, lint y formato, con resultados conservados.
5. Mantener la versión inicial disponible y todas las transformaciones trazables.
6. Declarar límites y contribución de IA sin inventar participación humana.

## Revisión por estándares y por especificación

<!-- revision -->

Los pedidos enviados y las respuestas están en docs/ia/revision_agentes.md.
El checklist completo y las acciones figuran en docs/code_review.md. Los
criterios externos de publicación y defensa siguen separados de la aceptación
técnica local; no se los marca como aprobados por ejecutar tests.

<!-- salto -->
# 9 Conclusiones y mejoras futuras

La comparación evidencia que calidad externa e interna requieren comprobaciones
diferentes. Las operaciones podían ejecutarse antes del cambio; la reorganización
reduce la dispersión de reglas y hace visible qué parte protege cada decisión.
El resultado se respalda mediante expectativas compartidas y casos de fallo.

El cambio de mayor valor estructural es separar persistencia de reglas y ubicar
las transiciones junto a Solicitud. Los objetos de parámetros expresan las
entradas de cada operación. Los enums reúnen vocabulario que antes se repetía.
No se midió productividad, por lo que no se atribuyen ahorros cuantitativos.

## Dificultades observadas

La captura de resultados mutables mostró que una demostración también puede
introducir errores. Conservar el test y su fallo permitió corregir la causa.
Otra dificultad fue mantener el orden de validación para que entradas inválidas
devuelvan los mismos mensajes. La revisión de tipos detectó incompatibilidades
locales que se corrigieron antes de fijar la base validada.

## Reflexión individual sobre el trabajo

La experiencia técnica deja una distinción defendible: refactorizar cambia la
estructura y requiere preservar reglas observables; agregar protección ante un
archivo corrupto amplía comportamiento y necesita verificación propia. Esta
reflexión resume los resultados del proceso asistido. El estudiante debe
revisarla y explicarla con sus palabras durante la defensa; no se afirma haber
comprobado todavía su aprendizaje o comprensión personal.

## Límites y próximos pasos

JSON local y max(id)+1 no garantizan registro concurrente. os.replace no es una
transacción de base de datos ni asegura durabilidad frente a pérdida de energía.
Para uso real se requerirían almacenamiento transaccional, autenticación,
autorización, auditoría y validación con usuarios. Son mejoras futuras y no
funcionalidades supuestamente incluidas en esta entrega.

El trabajo permite relacionar calidad y deuda de la unidad 1, pruebas y contratos
de la unidad 3, trazabilidad Git de la unidad 4 y comunicación y uso responsable
de IA de la unidad 5. No se incorporan patrones de diseño sin necesidad concreta.

<!-- salto -->
# 10 Trazabilidad y repositorio

| Hito | Referencia y propósito |
|---|---|
| Inicio de historial | Commit raíz vacío 5dbf789, base de revisión de toda la tarea |
| Sistema base | estado-inicial, commit 9428229, versión ejecutada y caracterizada |
| Diagnóstico | etapa-diagnostico, nueve debilidades con prioridad |
| Diseño y refactoring | etapa-refactoring, cinco transformaciones documentadas |
| Pruebas | etapa-pruebas, evidencias ejecutadas de verificación |
| Documentación | etapa-docs, cierre documental y guion |
| Estado final | estadorefactorizado, cierre técnico del conjunto |

El nombre estadorefactorizado se conserva tal como aparece en la consigna.
Los commits y tags tienen fechas reales del trabajo; no se inventa evolución
durante semanas anteriores. La contribución del único integrante se presenta
como trabajo individual con asistencia de IA declarada.

## Estructura del repositorio

```text
solicitudes/     Versión inicial, dominio, módulo, CLI y repositorios
tests/           Contratos, reglas, archivos y consola
docs/            Diagnóstico, refactorings, review y trazabilidad
docs/evidencias/ Salidas verificables de herramientas
docs/ia/         Registro de intercambios y revisión asistida
tools/           Verificación y construcción del informe
config_entrega.json  Enlaces reales cuando estén disponibles
```

Se conserva además una copia Git bundle recuperable dentro del anexo. A diferencia
de una carpeta de código sin .git, el bundle mantiene commits y tags. El README
explica cómo clonar el historial y ejecutar las dos versiones.

<!-- salto -->
# 11 Uso de inteligencia artificial

Se utilizó Codex de OpenAI como asistente en la aplicación de escritorio para
leer materiales, proponer el diseño, generar las dos versiones del prototipo,
crear pruebas, ejecutar comprobaciones, realizar revisión técnica asistida y
redactar informe y guion. El grado de intervención fue alto. No se describe
como simple corrección ortográfica ni se atribuye todo el código a escritura
manual previa del estudiante.

## Registro de intercambios relevantes

| Intercambio real | Decisión y evidencia |
|---|---|
| Pedido del estudiante de consultar materiales de la materia | Lectura de consigna, modelos y referencias de unidades 1, 3 y 4 |
| Respuesta: TPI completo, sistema base y refactorizado, informe, anexo y guion | Definición de entregables locales |
| Respuesta: usar el caso sugerido de solicitudes académicas | Selección del prototipo y alcance |
| Indicación: realizarlo con el estudiante como único integrante | Portada, identificación y guion individuales |
| Pedidos de revisión a dos agentes de IA | Reportes separados de estándares y especificación, con acciones |
| Autorización: publicarlo como repositorio público para la cátedra | Publicación real de main y los seis tags, con enlace incorporado al informe |

El registro detallado con citas literales, resúmenes identificados y resultados
se adjunta en docs/ia/registro.md y revision_agentes.md dentro del ZIP. No es
una exportación íntegra de la interfaz de chat ni contiene afirmaciones de
defensa, entrevistas o evaluación docente que no ocurrieron.

La IA no reemplaza la responsabilidad sobre lo entregado. Fermin Alliot debe
estudiar el código, ejecutar el sistema, revisar los argumentos y defender las
decisiones con voz propia. No se generó ni grabó una defensa sintética.

<!-- salto -->
# 12 Recursos de entrega y referencias

<!-- enlaces -->

## Anexo y video

El anexo ZIP incluye código, documentación, pruebas, evidencias de herramientas,
registro de IA, diagrama y bundle Git. El guion propone una defensa individual
de 12 a 14 minutos con cámara al comienzo y voz propia. Es una preparación para
grabar, no un video realizado. El video debe mostrar sistema, diagnóstico,
refactorings, pruebas, revisión y conclusiones.

Antes de subir la entrega se deben comprobar permisos y accesibilidad de ambos
enlaces. La consigna considera entregado el TPI cuando están cargados PDF,
repositorio, ZIP y video. La preparación local no reemplaza esa condición.

## Fuentes de la cátedra

1. TP MS2V2.pdf, páginas 1 a 6. Consigna oficial, requisitos y evaluación.
2. Guia_rapida_presentacion_TPI_MSII.docx, Modelo_Presentacion_TPI_MSII.pptx y README del modelo. Orden de exposición orientativo.
3. SEMANA_1_CALIDAD.pdf, unidad 1, páginas 4 y 5. Deuda técnica y smells.
4. SEMANA_II_SOLID.pdf, unidad 1. Responsabilidades y dependencias.
5. SEMANA_III_CLEAN_CODE.pdf, unidad 1, páginas 3 y 4. Refactoring y revisión técnica.
6. Semana 2.pdf, unidad 3, páginas 1 y 5. Pruebas, AAA y regresión.
7. MdS II UNIDAD 4 Semana 1.pdf. Objetos, historial y tags Git.

Las fuentes se consultaron en la carpeta de Metodología de Sistemas 2 indicada
por el estudiante. Los archivos de la cátedra no fueron modificados ni se
redistribuyen completos en el anexo. El análisis específico corresponde al
código y a las ejecuciones de este prototipo.
