# Code review y criterios de aceptación

La revisión tiene dos pasadas sobre el mismo checklist:

1. Revisión automatizada durante la construcción, con dos agentes de IA
   (ejes de estándares y de especificación). Sus hallazgos son CR01 a CR06 y
   el detalle de pedidos y respuestas está en docs/ia/revision_agentes.md.
2. Mi revisión manual del código final (Fermín Alliot), registrada en la
   sección "Revisión del autor", con observaciones CR07 en adelante.

Alcance: desde el commit raíz 5dbf789 hasta el tag estadorefactorizado.
Fuente de requisitos: docs/alcance.md y TP MS2V2.pdf. Ninguna de las dos
pasadas equivale a una aprobación de la cátedra.

## Checklist aplicado

| Criterio | Evidencia | Estado técnico |
|---|---|---|
| Cinco operaciones observables y tres entidades | catálogo, contrato y demo | Verificado por pruebas |
| Registro válido y rechazo sin escritura | contrato compartido y prueba de consola | Verificado por pruebas |
| Reglas completas de estados y responsable | matriz de 16 pares y contrato | Verificado por pruebas |
| No exposición de estado mutable final | dataclass frozen y copia de listar | Verificado por pruebas |
| Repositorio inyectado y dos implementaciones usadas | ModuloSolicitudes y pruebas de contrato | Verificado por inspección y pruebas |
| Archivo base compatible y acentos conservados | test_cli y test_repositorios | Verificado por pruebas |
| Fallo de reemplazo preserva datos | prueba con OSError simulado | Verificado por pruebas |
| Errores de dominio y persistencia distinguibles | CLI, códigos 2 y 3 | Verificado por pruebas |
| Nombres y responsabilidades claros | dominio, módulo, repositorios y consola | Revisado; copia inicial conservada con sus defectos |
| Sin secretos ni datos operativos reales | catálogos sintéticos y revisión del diff | Verificado por inspección |
| Nueve debilidades y cinco transformaciones trazables | diagnóstico y refactorings | Documentado |
| Uso de IA declarado como copiloto | docs/ia y guion | Documentado según Unidad 5 |
| Publicación GitHub y enlace del video | config_entrega.json y publicacion.md | GitHub público verificado; video provisto junto a la entrega |

Los resultados ejecutables definitivos figuran en docs/evidencias/validacion.json.
El repositorio público está enlazado y el paquete de entrega verificado. El enlace al
video de defensa grupal se entrega de forma adjunta según los requerimientos de la cátedra.

## Observaciones y feedback

| ID | Observación objetiva | Acción y criterio de cierre |
|---|---|---|
| CR01 | La primera prueba de comparación de demos falló: resultados anteriores apuntaban al mismo diccionario mutable inicial y cambiaban durante la demo | Capturar deepcopy de cada resultado en la presentación; test_demo_identica_en_ambas_versiones pasó al reejecutar. No se modificó la regla ni se relajó la prueba. Fallo original conservado en incidencia_demo_mutable.txt |
| CR02 | Mypy detectó incompatibilidades de tipos locales al construir el prototipo | Precisar el diccionario nueva y la variable opcional de búsqueda. Verificado con mypy antes de fijar estado-inicial. Commit 9428229 |
| CR03 | Una escritura directa podría truncar el archivo | RepositorioJson usa temporal y reemplazo; test_fallo_de_reemplazo_preserva_archivo_y_limpia_temporal comprueba datos y limpieza |
| CR04 | Un JSON mal formado no debe interpretarse como repositorio vacío | Validar estructura, enums, IDs y referencias; rechazar con ErrorPersistencia sin sobrescribir. Verificado con archivos inválidos |
| CR05 | La revisión de estándares detectó que una Solicitud construida directamente con ID cero o referencias inválidas podía guardarse en JSON y no volver a leerse | Validar invariantes en Solicitud.__post_init__, reutilizarlas al cargar JSON y probar construcción inválida. Se elimina la duplicación de reglas del deserializador |
| CR06 | La revisión de especificación detectó que el informe tenía salidas textuales pero no capturas | Incorporar capturas del panel documental local con fuentes de logs explícitas y sin presentarlo como una GUI del producto |

## Revisión por dos ejes

La skill code-review se aplicó a la base completa. Pedidos enviados, reportes
de estándares y de especificación, acciones y límites se conservan en
docs/ia/revision_agentes.md. Esa pasada es feedback técnico automatizado; mi
revisión manual se registra aparte, en la sección siguiente. Los defectos
atribuibles al trabajo se corrigen; las limitaciones deliberadas del alcance
se explican sin prometer resolverlas.

## Revisión cruzada del equipo (Code Review entre pares)

Revisores: Fermín Alliot y Gabriel Antuña. Fecha: 31 de octubre de 2026.
Versión revisada: tag estadorefactorizado (commit 58a18e4).
Procedimiento: Inspección cruzada del código siguiendo el checklist técnico,
contraste con las especificaciones de docs/alcance.md y ejecución local de la suite.

Cada fila indica qué se revisó, dónde y con qué criterio. En "Resultado" se registra
la conclusión técnica del equipo: Aceptado (cumple el criterio con justificación),
Observación (se documenta como límite o mejora futura) o Corregido.

| ID | Área y criterio | Ubicación | Pregunta de revisión | Resultado | Acción o justificación |
|---|---|---|---|---|---|
| CR07 | Nombres que revelan intención (Clean Code, cap. 2) | modulo.py ModuloSolicitudes; cli.py parser(); dominio.py E; repositorios.py _entero, _texto | ¿Cada nombre dice qué es o qué hace sin leer su cuerpo? | Aceptado | Los nombres en modulo.py, cli.py y repositorios.py son autoexplicativos. En dominio.py, E es un TypeVar acotado a StrEnum que usa convertir_enum para conservar el tipo concreto del enum; su alcance es local y es convención habitual para variables de tipo. |
| CR08 | Responsabilidad única de la consola (SRP) | cli.py ejecutar, líneas 53 a 96 | La función conoce las dos implementaciones (isinstance GestorInicial) y despacha por args.comando. ¿Se justifica por la comparación antes/después o es un Repeated Switch a corregir? | Aceptado con justificación | Se justifica estrictamente por la necesidad didáctica de comparar ambas versiones (inicial vs refactorizada) mediante el flag --implementacion. En producción se eliminaría para usar solo la versión modular. |
| CR09 | Manejo de errores | dominio.py líneas 75 a 132; cli.py main, líneas 147 a 149 | Todos los errores de dominio son ValueError y la consola los traduce a código 2. ¿Un ValueError que no sea de dominio podría informarse como error de negocio? ¿Conviene una excepción propia? | Observación | Actualmente es seguro y consistente para la CLI. Se documenta como mejora futura introducir excepciones de dominio específicas (DominioError, TransicionInvalidaError) para desacoplar de ValueError genérico. |
| CR10 | Duplicación de reglas | dominio.py Solicitud.asignar línea 121 y __post_init__ líneas 112 a 116 | El responsable inexistente se valida en dos lugares. ¿Es redundancia o cada chequeo protege un caso distinto? | Aceptado | No es redundancia viciosa: __post_init__ protege la invariante en la instanciación de cualquier entidad Solicitud, mientras asignar valida la transición en la operación de reasignación. |
| CR11 | Dependencias del dominio (DIP) | dominio.py línea 7, importación de catalogos | El dominio depende de los catálogos fijos. ¿Es aceptable en este alcance o limita las pruebas y la evolución? | Aceptado para el alcance | En este prototipo los catálogos son estructuras inmutables en memoria. En una evolución hacia base de datos se inyectará una interfaz ICatalogoRepositorio. |
| CR12 | Correspondencia con la especificación | alcance.md punto 2 frente a Solicitud.asignar | El alcance permite reasignar mientras la solicitud está abierta o en proceso. ¿El código hace exactamente eso y lo cubre una prueba? | Aceptado | Verificado: Solicitud.asignar permite cambiar responsable en abierta y en_proceso, y rechaza en resuelta o cancelada. Cubierto por test_asignar_responsable. |
| CR13 | Límites documentados | modulo.py registrar, línea 20 (max + 1); repositorios.py _cargar | IDs por max + 1 y relectura del archivo en cada operación. ¿Están declarados como límites en el informe y son razonables para la escala del caso? | Aceptado como límite | Declarado formalmente en la sección de límites del informe. Para un sistema monousuario local educativo es suficiente y evita dependencias de motores SQL externos. |
| CR14 | Calidad de las pruebas | tests/test_contrato.py | ¿Cada test sigue Arrange-Act-Assert, su nombre describe el comportamiento y el mismo contrato se aplica a ambas versiones? | Aceptado | Los tests aplican AAA rigurosamente, tienen nombres descriptivos en español y la clase ContratoSolicitudesTest valida indistintamente la versión inicial y refactorizada. |
| CR15 | Preservación de la versión base | git diff estado-inicial estadorefactorizado -- solicitudes/inicial.py | ¿La salida está vacía, es decir, la base sigue idéntica para la comparación? | Aceptado | La salida del diff está vacía (código 0). La versión inicial.py se preservó sin modificaciones tras el hito de estado-inicial. |

Criterio de cierre: una observación queda cerrada cuando está Aceptada con
justificación, documentada como límite en el informe o corregida con un commit
que mantiene la suite completa en PASS.

## Lectura de comentarios y docstrings

La revisión documental del 31 de octubre de 2026 comprobó ambas versiones:
no se encontraron marcas Generated by, referencias a LLM ni atribuciones a un
asistente dentro de solicitudes/. Los docstrings describen propósito, dominio,
invariantes o contrato de almacenamiento. Se conservaron; inicial.py permanece
idéntico al tag base. La declaración de herramientas se concentra en la
documentación y no se duplica como encabezado de los módulos.
