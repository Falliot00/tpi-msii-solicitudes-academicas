# Referencias técnicas y aplicación al caso

Consulta de las fuentes públicas: 31 de octubre de 2026. Las relaciones con este
prototipo son aplicaciones razonadas; las fuentes no evalúan ni certifican su código.
La consigna de la cátedra conserva prioridad sobre los modelos orientativos.

## Fowler: transformaciones y preservación de comportamiento

Fowler distingue el refactoring de una reestructuración general por el uso de
transformaciones pequeñas que preservan el comportamiento. En este caso se
contrastan expectativas comunes de las dos versiones y se separan las nuevas
garantías de persistencia de las transformaciones internas.
Fuente: [Refactoring Malapropism](https://martinfowler.com/bliki/RefactoringMalapropism.html), 2004.

| Decisión aplicada | Referencia del catálogo | Justificación específica |
|---|---|---|
| R01: extraer validación | [Extract Function / Extract Method](https://refactoring.com/catalog/extractFunction.html) | Nombrar la regla de estudiante y asunto y reducir la mezcla de acciones |
| R02: reubicar transiciones | [Move Function / Move Method](https://refactoring.com/catalog/moveFunction.html) | Localizar la regla junto al estado de Solicitud; el módulo conserva la coordinación |
| R03: entradas por operación | [Introduce Parameter Object](https://refactoring.com/catalog/introduceParameterObject.html) | Agrupar datos que viajan juntos y evitar parámetros de acciones ajenas |
| R04: extraer almacenamiento | [Extract Class](https://refactoring.com/catalog/extractClass.html) | Separar la gestión de archivos y la búsqueda por ID de las reglas del caso |
| R05: proteger representaciones y colección | [Replace Primitive with Object](https://refactoring.com/catalog/replacePrimitiveWithObject.html) y [Encapsulate Collection](https://refactoring.com/catalog/encapsulateCollection.html) | Concentrar vocabulario e impedir mutaciones externas; se adaptan las ideas a enums, dataclass frozen y copias |

R05 combina técnicas; usar enums por sí solo no equivale a implementar todos los
ejemplos del catálogo. El reemplazo atómico y el rechazo de archivos dañados
agregan garantías ante fallos y se verifican como mejoras adicionales.

## Martin: Clean Code y SOLID

[Clean Code: A Handbook of Agile Software Craftsmanship](https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884),
Robert C. Martin, Pearson, publicado en 2008, ISBN 9780132350884. Los capítulos
2, 3, 4 y 7 tratan nombres, funciones, comentarios y manejo de errores. En el caso
se aplican nombres del dominio, operaciones enfocadas y errores diferenciados.
Los docstrings documentan propósito y contrato; no se añaden comentarios que
repitan instrucciones evidentes.

[The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html),
Martin, 2014, fundamenta separar responsabilidades que responden a cambios
diferentes. La separación de persistencia, reglas y presentación es la aplicación
concreta en este prototipo, sin atribuirle una estructura organizacional real.

[Solid Relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html),
Martin, 2020, desarrolla los cinco principios. La siguiente tabla interpreta su
aplicación y registra qué evidencia permite evaluarla.

| Principio | Aplicación al prototipo | Evidencia y límite |
|---|---|---|
| SRP | Separar dominio, coordinación, almacenamiento y consola | Cada responsabilidad tiene ubicación concreta; no implica una clase por método |
| OCP | Cambiar el almacenamiento mediante un adaptador | Memoria y JSON se usan realmente; nuevas reglas pueden exigir cambios de dominio |
| LSP | Respetar el significado de listar, obtener y guardar | Contrato común y errores de ausencia; JSON tiene fallos de I/O documentados |
| ISP | Mantener pequeña la interfaz de almacenamiento | Solo tres operaciones utilizadas; no hay interfaces para necesidades hipotéticas |
| DIP | Inyectar RepositorioSolicitudes en el módulo | El código de coordinación depende del Protocol y no de rutas o archivos |

Estas referencias justifican criterios de diseño. La evidencia de que el cambio
conserva las reglas procede de los tests y ejecuciones del repositorio, no de citar
un autor. No se infiere ausencia de errores ni mejora cuantitativa sin medición.
