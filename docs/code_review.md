# Code review y criterios de aceptación

Revisión técnica asistida por IA. No constituye revisión de un compañero ni
aprobación de la cátedra. Se considera el trabajo desde el commit raíz vacío
5dbf789, incluyendo commits, archivos nuevos y cambios pendientes al revisar.
Fuente de requisitos: docs/alcance.md y TP MS2V2.pdf.

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
| Uso de IA declarado y guion con voz propia | docs/ia y guion | Documentado; grabación pendiente |
| Publicación GitHub y URL del video accesibles | config_entrega.json | Pendiente de publicación real |

Los resultados ejecutables definitivos figuran en docs/evidencias/validacion.json.
No se aprueba el conjunto documental completo mientras falten los enlaces y la
grabación. Los criterios técnicos pueden verificarse localmente por separado.

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

La skill code-review se aplica a la base completa. Pedidos enviados, reportes
de estándares y de especificación, acciones y límites se conservan en
docs/ia/revision_agentes.md. Sus hallazgos son feedback técnico de IA, no autoría
ni revisión humana. Los defectos nuevos atribuibles a esta tarea se corrigen;
las limitaciones deliberadas del alcance se explican sin prometer resolverlas.
