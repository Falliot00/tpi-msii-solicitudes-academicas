# Guion para la defensa individual

Fermin Alliot, legajo 101414, comisión M25 C4-02. Duración prevista: 12 a 14
minutos, incluyendo ejecución en vivo. El tiempo es una planificación, no una
grabación realizada. Usar cámara al inicio y voz propia durante toda la defensa.
Adaptar la redacción a la forma personal de explicar y ensayar los comandos.

## 00:00 a 00:45 Presentación con cámara

"Soy Fermin Alliot, legajo 101414, de la comisión M25 C4-02 de la Tecnicatura
Universitaria en Programación a Distancia. Presento mi Trabajo Práctico Integrador
de Metodología de Sistemas II. El trabajo analiza un prototipo de solicitudes
académicas para mejorar su calidad interna y verificar su comportamiento."

Mostrar portada. Explicar que el trabajo es individual y describir el uso de
IA en la implementación, las pruebas y la documentación, según la declaración
del informe. Presentar con palabras propias las decisiones que se van a defender.

## 00:45 a 02:00 Caso y alcance

"El sistema permite registrar una solicitud, asignar un responsable, cambiar su
estado, buscar por filtros y obtener un reporte. Usa estudiantes y responsables
ficticios. Se utiliza una consola y almacenamiento local para concentrar el
trabajo en diseño y verificación. El prototipo no tiene autenticación ni usuarios
simultáneos. Las tres estructuras principales son Estudiante, Responsable y
Solicitud. El estado inicial existe en Git y se puede ejecutar por separado."

Mostrar README y ejecutar:

```console
python -m solicitudes catalogos
python -m solicitudes --implementacion inicial demo
```

Señalar el ID, el responsable y el estado en_proceso, junto al reporte total 1.

## 02:00 a 03:20 Calidad externa e interna

"Desde la mirada del operador, el prototipo registra y consulta correctamente
los casos comprobados. Eso no alcanza para afirmar que su estructura sea fácil
de mantener. En GestorInicial, procesar reúne cinco operaciones y recibe diez
argumentos. También contiene validaciones, reglas de estado y escritura JSON.
Cambiar la persistencia obliga a editar el mismo módulo que las reglas."

Abrir solicitudes/inicial.py y docs/diagnostico.md. Mostrar el tag estado-inicial.
Explicar que los resultados funcionales se apoyan en pruebas, sin afirmar que
hubo una evaluación de usabilidad con usuarios reales.

## 03:20 a 05:00 Deuda técnica y smells

"Se registraron nueve debilidades. Para cada una se documentó evidencia, ubicación,
impacto, riesgo y prioridad. Los ejemplos más claros son el método con varias
responsabilidades, los parámetros excesivos, la búsqueda repetida, las cadenas
que representan estados y la colección mutable expuesta. Se priorizó proteger
las reglas y el almacenamiento antes de ampliar funcionalidades."

Mostrar D01, D04, D07 y D09. Explicar un costo concreto: agregar un estado exige
revisar transición, filtro y reporte en el código inicial. No leer toda la tabla.

## 05:00 a 07:20 Refactorings y principios

"Se aplicó Extract Method para aislar validación, se reubicaron las transiciones
en Solicitud y se introdujeron NuevaSolicitud y FiltroSolicitudes como objetos de
parámetros. Se extrajeron los repositorios y se agruparon los estados en enums.
Solicitud es inmutable, por lo que una operación devuelve un nuevo valor."

Mostrar solicitudes/dominio.py, modulo.py y repositorios.py. Seguir un cambio
de estado desde el módulo hasta la entidad. Usar docs/refactorings.md como apoyo.
Relacionar las transformaciones con Fowler y la separación de responsabilidades
con Martin, según docs/referencias_tecnicas.md. Explicar la aplicación al código.

"SRP separa reglas, coordinación, persistencia y consola. DIP aparece porque
el módulo recibe el contrato de repositorio. Los adaptadores de memoria y JSON
permiten comprobar sustitución dentro de ese contrato. OCP se aplica a cambiar
el almacenamiento sin editar reglas. No significa que agregar cualquier regla
no requiera modificar código. La interfaz tiene solo tres operaciones usadas."

## 07:20 a 09:30 Pruebas y demostración

Ejecutar en una carpeta de datos nueva para la grabación:

```console
python -m solicitudes --archivo datos/defensa.json registrar --estudiante 1 --asunto "Constancia para beca" --detalle "Ciclo 2026" --tipo constancia --prioridad alta
python -m solicitudes --archivo datos/defensa.json estado 1 en_proceso
python -m solicitudes --archivo datos/defensa.json asignar 1 1
python -m solicitudes --archivo datos/defensa.json estado 1 en_proceso
python -m solicitudes --archivo datos/defensa.json listar --estado en_proceso --prioridad alta
python -m solicitudes --archivo datos/defensa.json estado 1 resuelta
python -m solicitudes --archivo datos/defensa.json reporte
python -m unittest discover -s tests -v
```

Si defensa.json ya contiene datos, usar otra ruta nueva y tomar el ID que
devuelva registrar. El primer cambio de estado debe rechazarse porque falta
responsable. Señalar que ese rechazo es el comportamiento esperado.

"Las 13 pruebas de caracterización se aplican a ambas versiones. También se
verifican los 16 pares de estados, el contrato de almacenamiento, compatibilidad
del JSON, errores y conservación del archivo cuando falla el reemplazo.
Los resultados y comandos ejecutados están en docs/evidencias."

No decir que los tests garantizan ausencia de errores ni inventar cobertura.

## 09:30 a 11:00 Code review y trazabilidad

Mostrar docs/code_review.md, docs/trazabilidad.md y:

```console
git log --oneline --decorate
git tag --list
git diff estado-inicial estadorefactorizado -- solicitudes
```

"El checklist cubre reglas, errores, encapsulación, persistencia, pruebas y
documentación. La revisión técnica asistida por IA registró observaciones y
acciones. No la presento como revisión de un compañero humano. Cada hito tiene
un tag y se conserva el archivo inicial para comparar."

Explicar un hallazgo real del registro de revisión y la corrección comprobada.

## 11:00 a 12:30 Conclusiones y límites

"El resultado principal es que las reglas quedan localizadas y se pueden
probar mediante una interfaz pequeña. El sistema conserva las operaciones
comprobadas y mejora la protección del archivo. El límite más importante es
que JSON local no admite concurrencia segura: max(id)+1 y el reemplazo de
archivo no equivalen a una transacción de base de datos."

Explicar con palabras propias una dificultad concreta y un aprendizaje que
realmente se haya comprendido. Proponer como trabajo futuro una base de datos
con transacciones y autenticación, si el sistema fuera a usarse de verdad.

## Preparación y publicación

- Ensayar desde una copia del repositorio, verificar pantalla legible y audio.
- Estudiar por qué una transición se acepta o rechaza y cómo se conserva JSON.
- Grabar con voz propia. No usar síntesis de voz ni un avatar como defensa.
- Subir el video, comprobar acceso y colocar su URL en config_entrega.json.
- La URL GitHub ya está cargada. Comprobar su acceso y regenerar informe y anexo al agregar el video.

## Preguntas para practicar

1. ¿Por qué un sistema que funciona puede tener deuda técnica?
2. ¿Cuál es la diferencia entre mover una regla y cambiar su comportamiento?
3. ¿Qué demuestra la matriz de estados y qué no demuestra?
4. ¿Cómo se aplica DIP sin una base de datos real?
5. ¿Qué sucede si dos procesos registran al mismo tiempo?
6. ¿Por qué la escritura atómica es una mejora adicional y no un refactoring puro?
7. ¿Qué decisiones sugeridas por IA podés justificar y cuáles revisarías?
