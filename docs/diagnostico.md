# Diagnóstico del estado inicial

Referencia estable: tag estado-inicial, commit 9428229. Archivo
solicitudes/inicial.py. Los problemas se observan en el prototipo educativo;
no se afirma que hayan causado incidentes reales. Prioridad alta significa
corregir antes de ampliar el módulo; media, reducir costo de cambio.

| ID | Debilidad y evidencia | Ubicación inicial | Impacto y riesgo | Prioridad | Acción prevista |
|---|---|---|---|---|---|
| D01 | Long Method: procesar decide registro, asignación, transición, consulta y reporte | procesar, líneas 22 a 116 | Hay que recorrer ramas ajenas para modificar una operación; regresión entre casos | Alta | Separar operaciones y extraer validación |
| D02 | Long Parameter List: diez argumentos además de self, la mayoría irrelevantes según acción | firma de procesar, líneas 22 a 34 | Llamadas confusas y combinaciones sin significado; orden erróneo de datos | Media | NuevaSolicitud y FiltroSolicitudes |
| D03 | Primitive Obsession: estados, tipos y prioridades son cadenas libres en diccionarios | registro y validaciones, líneas 39 a 51 y 80 a 86 | Errores de escritura y reglas dispersas; no hay vocabulario tipado central | Alta | Enums y Solicitud inmutable |
| D04 | Duplicated Code: búsqueda lineal con variable s y mismo error | ramas asignar y estado, líneas 57 a 64 y 72 a 79 | Una corrección debe repetirse; manejo de ausentes puede divergir | Media | Repositorio.obtener |
| D05 | Responsabilidades divergentes: GestorInicial valida, cambia estados, filtra, reporta y escribe JSON | procesar y _guardar | Un cambio de almacenamiento afecta el mismo módulo que las reglas; difícil simular fallos | Alta | Extraer repositorio e inyectarlo |
| D06 | Nombres poco expresivos: s, r, p y accion con significados dependientes de la rama | bucles y mapa de transiciones | Más esfuerzo de lectura y revisión; confundir estado y registro | Media | Nombres del dominio y operaciones explícitas |
| D07 | Estado mutable expuesto: self.datos es público y se devuelve el diccionario almacenado | __init__, return nueva, return s y listar | Un consumidor Python puede saltarse validaciones al modificar una referencia | Alta | Entidades frozen y copias de la colección |
| D08 | Conocimiento duplicado de catálogos: literales de tipos/prioridades en registro y filtros, estados en transición/filtro/reporte | procesar, líneas 39 a 42, 80 a 86, 95 a 100 y 113 | Agregar un valor obliga a revisar varias ramas; omisión en reporte | Media | Centralizar vocabulario en enums |
| D09 | Escritura directa sobre el archivo existente, sin reemplazo atómico | _guardar, líneas 118 a 124 | Un fallo durante escritura puede truncar datos; riesgo de pérdida local | Alta | Archivo temporal en la misma carpeta y os.replace |

D01 a D08 son señales de diseño o debilidades de encapsulación; D09 es una
debilidad de implementación. Los nombres de smells son heurísticas: la longitud
por sí sola no demuestra mala calidad. Aquí D01 se justifica por las cinco
responsabilidades presentes en el mismo flujo. D05 no se denomina God Class,
porque el tamaño de este prototipo no justifica esa etiqueta.

## Calidad externa e interna

Las 13 pruebas de caracterización verifican registro, identificadores, datos
inválidos, ciclo de estados, responsable obligatorio, saltos, idempotencia,
cierre, referencias, filtros, reportes y recuperación desde archivo. La demo
inicial registra, asigna, avanza a en_proceso y produce un reporte coherente.
Esto respalda un comportamiento funcional acotado, no usabilidad validada con
estudiantes reales. Internamente se observan los nueve problemas de la tabla.

## Costo del cambio

Cambiar el almacenamiento obliga a editar GestorInicial; incorporar un estado
afecta transición, filtros y reporte. Son riesgos concretos de mantenimiento.
No se estiman horas ahorradas ni porcentajes de productividad sin mediciones.
