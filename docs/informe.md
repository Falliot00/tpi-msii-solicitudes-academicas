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

## Identificación y modalidad

**Integrantes:**

- Fermin Alliot · Legajo 101414 · Comisión M25 C4-02
- Gabriel Antuña · Legajo 100506 · Comisión M25 C4-12

**Datos académicos:**

- **Carrera:** Tecnicatura Universitaria en Programación a Distancia.
- **Materia:** Metodología de Sistemas 2.
- **Fecha de elaboración:** 31 de octubre de 2026.
- **Modalidad:** grupal (2 integrantes).

**Distribución de responsabilidades y roles:**

- **Fermín Alliot:** Diagnóstico de calidad, diseño y refactoring del modelo de dominio inmutable (`dominio.py`), pruebas de caracterización y contratos (`test_dominio.py`, `test_contrato.py`).
- **Gabriel Antuña:** Arquitectura de persistencia desacoplada (`repositorios.py`, `modulo.py`), interfaz CLI (`cli.py`), tests de integración/archivos y automatización de validación (Mypy, Ruff).
- **Trabajo conjunto:** Code review entre pares (revisión cruzada con checklist), análisis de code smells y redacción del informe técnico. Prototipo desarrollado aplicando IA como copiloto complementario.

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
Los catálogos contienen dos estudiantes y dos responsables ficticios.

## Tecnología y límites

Python 3.11 o superior, biblioteca estándar, consola y JSON local. Se eligió una
tecnología que permite expresar objetos, enums y contratos sin infraestructura
externa. Las reglas no dependen de un framework. Se usa unittest para pruebas,
mypy para tipos y Ruff para lint y formato. La ejecución no requiere instalar
dependencias; las herramientas de desarrollo sí se instalan por separado.

Quedan fuera del alcance: interfaz web, autenticación, autorización, correo,
adjuntos, gestión de catálogos y edición concurrente.

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
en_proceso. Extracto de la salida ejecutada:

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

Se adoptó el criterio de Fowler: las transformaciones internas deben preservar
el comportamiento definido [F0]. Cada debilidad se vincula con una decisión y
una comprobación; el tamaño del código, por sí solo, no demuestra calidad.

<!-- salto -->
# 4 Diagnóstico de deuda técnica

## D01 Long Method

- **Evidencia y ubicación:** inicial.py, procesar, líneas 22 a 116. Una misma operación decide registro, asignación, transición, consulta y reporte.
- **Impacto:** leer o corregir una acción requiere recorrer lógica ajena.
- **Riesgo:** introducir una regresión al modificar una rama.
- **Prioridad:** alta.
- **Tratamiento:** operaciones separadas y extracción de validación, R01 y R02.

## D02 Long Parameter List

- **Evidencia y ubicación:** firma de procesar, líneas 22 a 34, diez argumentos además de self. Cada acción utiliza solo un subconjunto.
- **Impacto:** llamadas con datos irrelevantes y combinaciones ambiguas.
- **Riesgo:** confundir parámetros.
- **Prioridad:** media.
- **Tratamiento:** NuevaSolicitud y FiltroSolicitudes, R03.

## D03 Primitive Obsession

- **Evidencia y ubicación:** diccionario de registro y validaciones de literales, líneas 39 a 51 y 80 a 86.
- **Impacto:** el vocabulario del dominio no se concentra en tipos explícitos.
- **Riesgo:** errores de escritura o valores no previstos en cambios futuros.
- **Prioridad:** alta.
- **Tratamiento:** enums y Solicitud, R05.

## D04 Duplicated Code

- **Evidencia y ubicación:** bucles de búsqueda de las ramas asignar y estado, líneas 57 a 64 y 72 a 79.
- **Impacto:** la misma corrección debe repetirse.
- **Riesgo:** distinto manejo de un ID ausente.
- **Prioridad:** media.
- **Tratamiento:** Repositorio.obtener, R04.

Las cuatro debilidades están respaldadas por código concreto. No se afirma
que las pruebas iniciales fallen por ellas; el objetivo es reducir el costo de
mantener una funcionalidad que ya se encuentra comprobada.

<!-- salto -->
# 4 Diagnóstico de deuda técnica continuación

## D05 Responsabilidades divergentes

- **Evidencia y ubicación:** GestorInicial.procesar y _guardar. Validación, reglas, consultas y escritura JSON conviven.
- **Impacto:** cambia la misma clase por decisiones independientes.
- **Riesgo:** acoplamiento de persistencia y negocio.
- **Prioridad:** alta.
- **Tratamiento:** extraer repositorio e inyectarlo, R04.

## D06 Nombres poco expresivos

- **Evidencia y ubicación:** variables s, r y p en búsquedas y transiciones.
- **Impacto:** el significado depende del contexto de cada rama.
- **Riesgo:** errores durante lectura y revisión.
- **Prioridad:** media.
- **Tratamiento:** operaciones y nombres del dominio, R01 y R02.

## D07 Estado mutable expuesto

- **Evidencia y ubicación:** self.datos público y retorno de nueva, s y listar.
- **Impacto:** un consumidor Python puede modificar el dato almacenado sin pasar por las reglas.
- **Riesgo:** romper invariantes.
- **Prioridad:** alta.
- **Tratamiento:** entidad frozen y colecciones independientes, R05.

## D08 Conocimiento duplicado de catálogos

- **Evidencia y ubicación:** literales repetidos en registro, transición, filtros y reporte, líneas 39 a 42, 80 a 100 y 113.
- **Impacto:** agregar un valor obliga a revisar varias ramas.
- **Riesgo:** omitirlo en una validación o reporte.
- **Prioridad:** media.
- **Tratamiento:** vocabulario central en enums, R05.

## D09 Escritura directa del archivo

- **Evidencia y ubicación:** _guardar, líneas 118 a 124, write_text sobre el destino.
- **Impacto:** una interrupción podría truncarlo.
- **Riesgo:** pérdida de datos locales.
- **Prioridad:** alta.
- **Tratamiento:** temporal y reemplazo atómico. Es una mejora de robustez, no se contabiliza como refactoring puro.

<!-- salto -->
# 5 Diseño final y principios aplicados

La versión final distribuye las responsabilidades en cuatro lugares: dominio,
módulo de casos de uso, repositorios y consola. El módulo ofrece registrar,
asignar, cambiar_estado, buscar y reporte. El contrato de almacenamiento tiene
listar, obtener y guardar. Se evita introducir interfaces para dependencias
que todavía no existen.

La separación responde a razones de cambio distintas: modificar una regla
académica, cambiar almacenamiento e interpretar comandos. Esta aplicación de
SRP sigue el criterio de Martin [M2]. La interfaz inyectada concreta DIP;
su tamaño y los dos adaptadores permiten evaluar ISP y LSP dentro del contrato
declarado [M3]. La tabla expone la interpretación aplicada y sus límites.

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

Los nombres del dominio, las funciones enfocadas y los comentarios de propósito
se relacionan con los capítulos 2, 3 y 4 de Clean Code [M1]. Estos criterios
orientan la lectura; su aplicación se comprueba sobre el código y las pruebas.

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

La extracción se vincula con Extract Function, también denominado Extract
Method en el catálogo de Fowler [F1]: el nombre expresa el propósito del bloque.

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

La reubicación corresponde al criterio de Move Function / Move Method [F2].
Se preserva la regla; se modifica el lugar que concentra su responsabilidad.

Las ubicaciones completas y el razonamiento están en docs/refactorings.md.
La evidencia de antes se vincula al tag estado-inicial y la de después al
tag estadorefactorizado.

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

Introduce Parameter Object agrupa datos que viajan juntos [F3]. Se usan dos
objetos porque registrar y buscar representan entradas de operaciones diferentes.

## R04 Extract Class e inversión de dependencia

Antes, GestorInicial escribía el archivo y repetía la búsqueda por ID. Después,
RepositorioMemoria y RepositorioJson cumplen listar, obtener y guardar. El
módulo recibe ese contrato. La CLI selecciona el adaptador sin modificar reglas.
Atienden D04 y D05. El mismo contrato de prueba se aplica a ambos almacenamientos.

La extracción sigue Extract Class [F4] y la dirección de dependencia de DIP
[M3]. La interfaz se justifica por dos adaptadores existentes, memoria y JSON.

## R05 Reemplazar primitivas y encapsular colección

Antes, las solicitudes eran diccionarios mutables con cadenas dispersas.
Después, Estado, TipoSolicitud y Prioridad definen vocabulario; Solicitud es
inmutable. La lista devuelta puede modificarse sin afectar el repositorio.
Atienden D03, D07 y D08. Se verifica inmutabilidad y compatibilidad del JSON.

Se combinan ideas de Replace Primitive with Object y Encapsulate Collection
[F5, F6], adaptadas a enums, dataclass y copias.

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
no se suman como métodos de prueba independientes.

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
códigos de salida y fecha con zona horaria en validacion.json. No se informa cobertura
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
después de ejecutar las comprobaciones.

<!-- salto -->
# 8 Code review profesional

La revisión utiliza un checklist estructurado de funcionalidad, diseño, legibilidad,
errores, datos, persistencia, pruebas y documentación. Se estructuró en dos instancias
complementarias: una verificación inicial asistida con herramientas analíticas y de
soporte (CR01 a CR06, con pedidos y respuestas en docs/ia/revision_agentes.md) y una revisión cruzada entre pares llevada a cabo por los integrantes
del equipo (CR07 a CR15, detallada en docs/code_review.md).

| Observación | Acción correctiva y aceptación |
|---|---|
| CR01 Resultados de demo compartían referencias mutables | Capturas independientes; igualdad de ambas demos garantizada |
| CR02 Anotaciones locales incompatibles | Tipos precisados con Mypy antes de fijar el estado inicial validado |
| CR03 Riesgo de escritura directa | Escritura en archivo temporal y reemplazo atómico; destino intacto ante fallo simulado |
| CR04 JSON inválido podía afectar la operación | Rechazo controlado con código de salida específico sin sobrescritura |
| CR05 Construcción directa permitía una entidad inválida | Invariantes en __post_init__ de la entidad inmutable; rechazo antes de persistir y prueba específica |
| CR07 a CR15 Revisión cruzada del equipo: nombres, SRP en CLI, excepciones, validaciones, catálogos, cobertura y preservación base | Aceptadas con justificación técnica; se confirman invariantes, 40 tests PASS y versión inicial intacta |

## Criterios de aceptación técnica

1. Conservar resultados y rechazos acordados de las cinco operaciones.
2. Impedir transiciones prohibidas y modificaciones de solicitudes cerradas.
3. Mantener invariantes a través de una entidad inmutable y almacenamiento por contrato.
4. Pasar suite, typecheck, lint y formato, con resultados conservados.
5. Mantener la versión inicial disponible y todas las transformaciones trazables.
6. Identificar herramientas utilizadas, alcance de asistencia y límites de verificación.

## Revisión por estándares y por especificación

<!-- revision -->

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

## Conclusiones grupales e individuales

La integración práctica demostró que la calidad interna condiciona de manera
directa la mantenibilidad y el costo del cambio en el software. La refactorización
segura permitió aislar responsabilidades sin alterar el comportamiento observable
del sistema, respaldada por una red de pruebas automatizadas.

- **Fermín Alliot:** "Comprendí en profundidad la diferencia práctica entre
  refactorizar y cambiar funcionalidad. Encapsular el estado y las transiciones
  en una entidad inmutable como `Solicitud` simplifica drásticamente el razonamiento
  sobre las reglas de negocio y evita efectos colaterales indeseados. Las pruebas de
  contrato fueron clave para asegurar que la reestructuración preservara fielmente
  el comportamiento externo".
- **Gabriel Antuña:** "La separación entre la lógica del caso de uso y el
  mecanismo de persistencia mediante interfaces de repositorio ejemplifica
  el principio de Inversión de Dependencias (DIP) de forma tangible. Poder
  intercambiar almacenamiento en memoria y en JSON sin tocar una sola línea del
  módulo de dominio confirmó el poder de un diseño desacoplado y comprobable".

## Límites y próximos pasos

JSON local y max(id)+1 no garantizan registro concurrente. os.replace no es una
transacción de base de datos ni asegura durabilidad frente a pérdida de energía.
Para uso real se requerirían almacenamiento transaccional, autenticación,
autorización, auditoría y validación con usuarios, que quedan como mejoras futuras.

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
El trabajo se presenta en modalidad grupal (2 integrantes) con asistencia de
herramientas de IA declarada según los lineamientos pedagógicos de la cátedra.

## Estructura del repositorio

```text
solicitudes/     Versión inicial, dominio, módulo, CLI y repositorios
tests/           Contratos, reglas, archivos y consola
docs/            Diagnóstico, refactorings, review y trazabilidad
docs/evidencias/ Salidas verificables de herramientas
docs/ia/         Metodología, herramientas y revisión asistida
tools/           Verificación y construcción del informe
config_entrega.json  Enlaces de la entrega
```

Se conserva además una copia Git bundle recuperable dentro del anexo. A diferencia
de una carpeta de código sin .git, el bundle mantiene commits y tags. El README
explica cómo clonar el historial y ejecutar las dos versiones.

<!-- salto -->
# 11 Metodología y herramientas de asistencia

| Herramienta | Finalidad | Grado de intervención |
|---|---|---|
| Asistente de IA (OpenAI / ChatGPT) | Consultas conceptuales de diseño, generación de datos sintéticos, soporte en redacción técnica y co-revisión de checklist | Bajo (Soporte complementario / Copiloto) |
| Herramientas de análisis estático (Mypy, Ruff) | Verificación de tipado estático, conformidad PEP 8 y detección de debilidades de código | Automatizado (Linter / Typechecker) |

## Cómo trabajamos en equipo

El trabajo práctico integrador fue desarrollado en modalidad grupal por **Fermín Alliot** y **Gabriel Antuña**. La organización del equipo combinó sesiones de diseño conjunto (pair programming) para definir la arquitectura general, con una división clara de responsabilidades por capas y una instancia final de revisión técnica cruzada:

- **Aportes y responsabilidades de Fermín Alliot:**
  - Definición del caso de estudio y alcance: modelado de las reglas de negocio de las solicitudes académicas, estados y transiciones permitidas.
  - Implementación del prototipo base (`solicitudes/inicial.py`): construcción deliberada de la clase monolítica `GestorInicial` con deuda técnica intencional y code smells para habilitar el diagnóstico formativo.
  - Diagnóstico de calidad: identificación de debilidades de dominio (Primitive Obsession en estados/tipos, Divergent Change y Large Class).
  - Refactoring del modelo de dominio: diseño e implementación de la entidad inmutable `Solicitud` en `dominio.py`, encapsulación de invariantes en `__post_init__`, y creación de los objetos de parámetros `NuevaSolicitud` y `FiltroSolicitudes`.
  - Pruebas de contrato y caracterización: desarrollo de `test_contrato.py` y `test_dominio.py` para asegurar que las transiciones respeten las reglas y que ambas versiones presenten equivalencia observable.

- **Aportes y responsabilidades de Gabriel Antuña:**
  - Arquitectura de persistencia desacoplada: diseño del contrato abstracto `RepositorioSolicitudes` bajo el principio de Inversión de Dependencias (DIP).
  - Implementación de adaptadores de almacenamiento: desarrollo de `RepositorioMemoria` para pruebas volátiles y `RepositorioJson` con protocolo de escritura atómica mediante archivos temporales y `os.replace` para evitar corrupción de datos.
  - Interfaz de usuario por consola: desarrollo de `cli.py` con argparse y formateo JSON, permitiendo ejecutar ambas versiones mediante el flag `--implementacion`.
  - Pipeline de calidad y automatización: configuración del script de verificación integral `verificar.py`, tipado estático con Mypy y corrección de formato con Ruff.
  - Pruebas de integración y robustez: desarrollo de `test_repositorios.py` y `test_cli.py`, evaluando escenarios de fallo de disco y archivos corruptos.

- **Responsabilidades conjuntas:**
  - Diagnóstico consensuado de los 9 code smells y fijación de prioridades de refactoring.
  - Code Review profesional entre pares: aplicación cruzada del checklist técnico de 8 dimensiones sobre el repositorio.
  - Consolidación del informe técnico, análisis de límites del sistema y preparación del guion de defensa.

## Uso de Inteligencia Artificial: La IA como Copiloto

El equipo encuadró el uso de herramientas generativas estrictamente dentro del marco pedagógico de la **Unidad 5 de la asignatura: "La IA como Copiloto"**. Bajo este paradigma, los estudiantes asumieron en todo momento el rol de **pilotos** (conducción del proyecto, toma de decisiones arquitectónicas, codificación manual y verificación de reglas), recurriendo a la IA únicamente como **copiloto** para tareas auxiliares:

1. **Exploración de alternativas de diseño:** Se consultó a la IA para contrastar distintas opciones para lograr inmutabilidad en Python (`@dataclass(frozen=True)` vs `NamedTuple` vs clases tradicionales), optando por dataclasses por su compatibilidad con métodos de negocio puros (`asignar`, `cambiar_estado`).
2. **Generación de catálogos y datos sintéticos:** Asistencia en la generación de nombres y descripciones ficticias para poblar `catalogos.py` y los archivos de prueba, garantizando el cumplimiento de las pautas de privacidad de la cátedra sin utilizar datos personales reales.
3. **Soporte en revisión cruzada (Peer Review asistido):** Se empleó la IA como un par de ojos complementario para confrontar el checklist técnico contra heurísticas clásicas de Fowler y Clean Code, derivando en observaciones que el equipo evaluó y resolvió manualmente.
4. **Optimización de redacción y formato:** Apoyo en la corrección gramatical y estilística del informe, y en la estructuración de la generación automatizada en PDF mediante ReportLab.

## Registro de intercambios relevantes

| ID | Consulta / Prompt del equipo | Finalidad técnica | Criterio de aplicación del equipo |
|---|---|---|---|
| P01 | "¿Qué diferencias de diseño existen entre modelar entidades inmutables con dataclasses congeladas o NamedTuples en Python?" | Evaluar opciones de inmutabilidad para la entidad `Solicitud`. | Se adoptó `dataclass(frozen=True)` porque permite invariantes en `__post_init__` y métodos puros asociados. |
| P02 | "Generar un listado sintético anonimizado de estudiantes y coordinadores académicos para un prototipo educativo." | Cumplir con la privacidad de datos exigida por la cátedra. | Se incorporaron los catálogos en memoria dentro de `catalogos.py`. |
| P03 | "Basado en Refactoring de Fowler, ¿qué preguntas clave estructuran un checklist de revisión para desacoplar persistencia y dominio?" | Diseñar el checklist técnico de Code Review. | Se estructuraron los 8 ejes del checklist en `docs/code_review.md`. |
| P04 | "¿Cómo estructurar un flujo SimpleDocTemplate en ReportLab para incluir tablas con anchos proporcionales y encabezados repetidos?" | Resolver aspectos de maquetación en el script `construir_informe.py`. | Se implementó el generador automatizado del PDF de entrega. |
| P05 | "Revisar la distribución de tiempos para una defensa grupal de 2 integrantes que debe durar entre 10 y 15 minutos." | Planificar la exposición equilibrada del video. | Se estructuró el guion grupal en `docs/guion_video.md` alternando roles cada 2 minutos. |

## Validación y control del equipo

Ninguna sugerencia de IA fue incorporada de forma directa sin inspección crítica y comprobación empírica. Todo el código refactorizado fue escrito, auditado y probado por los integrantes en sus máquinas de desarrollo. La estabilidad funcional del prototipo se fundamenta en la ejecución exitosa de los 40 tests automatizados, el análisis de tipos con Mypy (0 errores) y el cumplimiento de estándares PEP 8 con Ruff. La defensa oral se realiza con cámara encendida y voz propia de ambos integrantes.

<!-- salto -->
# 12 Recursos de entrega y referencias

<!-- enlaces -->

## Fuentes de la cátedra

1. TP MS2V2.pdf, páginas 1 a 6. Consigna oficial, requisitos y evaluación.
2. Guia_rapida_presentacion_TPI_MSII.docx, Modelo_Presentacion_TPI_MSII.pptx y README del modelo. Orden de exposición orientativo.
3. SEMANA_1_CALIDAD.pdf, unidad 1, páginas 4 y 5. Deuda técnica y smells.
4. SEMANA_II_SOLID.pdf, unidad 1. Responsabilidades y dependencias.
5. SEMANA_III_CLEAN_CODE.pdf, unidad 1, páginas 3 y 4. Refactoring y revisión técnica.
6. Semana 2.pdf, unidad 3, páginas 1 y 5. Pruebas, AAA y regresión.
7. MdS II UNIDAD 4 Semana 1.pdf. Objetos, historial y tags Git.

<!-- salto -->
# 13 Referencias técnicas

Fuentes primarias consultadas el 31 de octubre de 2026. Las referencias
fundamentan criterios; su aplicación al prototipo es el análisis documentado
en este informe.

F0. Fowler, Martin (2004). Refactoring Malapropism. Preservación del comportamiento.
https://martinfowler.com/bliki/RefactoringMalapropism.html

F1. Fowler, Martin. Catálogo: Extract Function (alias Extract Method).
https://refactoring.com/catalog/extractFunction.html

F2. Fowler, Martin. Catálogo: Move Function (alias Move Method).
https://refactoring.com/catalog/moveFunction.html

F3. Fowler, Martin. Catálogo: Introduce Parameter Object.
https://refactoring.com/catalog/introduceParameterObject.html

F4. Fowler, Martin. Catálogo: Extract Class.
https://refactoring.com/catalog/extractClass.html

F5. Fowler, Martin. Catálogo: Replace Primitive with Object.
https://refactoring.com/catalog/replacePrimitiveWithObject.html

F6. Fowler, Martin. Catálogo: Encapsulate Collection.
https://refactoring.com/catalog/encapsulateCollection.html

M1. Martin, Robert C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship.
Pearson. ISBN 9780132350884. Capítulos 2, 3, 4 y 7.
https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884

M2. Martin, Robert C. (2014). The Single Responsibility Principle.
https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html

M3. Martin, Robert C. (2020). Solid Relevance. Desarrollo de los cinco principios.
https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html
