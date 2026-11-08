# Guion para la defensa grupal

Integrantes:
- **Fermín Alliot** · Legajo 101414 · Comisión M25 C4-02
- **Gabriel Antuña** · Legajo 100506 · Comisión M25 C4-12

Duración prevista: 12 a 14 minutos. Ambos integrantes se presentan con cámara encendida
al inicio y utilizan voz propia a lo largo de toda la exposición.

---

## 00:00 a 00:50 Presentación con cámara (Ambos integrantes)

**Fermín Alliot:**  
"Buenas tardes. Mi nombre es Fermín Alliot, legajo 101414, de la comisión M25 C4-02 de la
Tecnicatura Universitaria en Programación a Distancia."

**Gabriel Antuña:**  
"Y mi nombre es Gabriel Antuña, legajo 100506, de la comisión M25 C4-12. Juntos presentamos
nuestro Trabajo Práctico Integrador para Metodología de Sistemas II."

**Fermín Alliot:**  
"El trabajo aborda el análisis y evolución de un sistema de solicitudes académicas, partiendo
de un prototipo con funcionamiento externo pero con severos problemas de diseño interno,
aplicando diagnóstico de deuda técnica, principios SOLID, Clean Code, refactoring seguro,
una suite de pruebas de regresión y una revisión técnica entre pares."

---

## 00:50 a 02:20 Caso, alcance y sistema base (Fermín Alliot)

**Fermín Alliot:**  
"El sistema permite a un operador registrar solicitudes de estudiantes, asignarlas a
responsables de área, transicionar sus estados, filtrar listados y generar reportes simples.
Para concentrarnos en la calidad del diseño y la verificación sin dependencias complejas,
utilizamos almacenamiento local estructurado y catálogos sintéticos de estudiantes y áreas."

*(Mostrar README y ejecutar en consola):*
```console
python -m solicitudes catalogos
python -m solicitudes --implementacion inicial demo
```

"Vemos que el sistema base responde y realiza las operaciones. Sin embargo, si miramos
el código en `solicitudes/inicial.py` correspondiente al tag `estado-inicial`, encontramos
que una única clase `GestorInicial` concentra la validación de argumentos, las transiciones de
estados, el formateo y la escritura en archivo JSON."

---

## 02:20 a 04:00 Calidad externa vs interna y Code Smells (Gabriel Antuña)

**Gabriel Antuña:**  
"Esta discrepancia ilustra el núcleo de la materia: **calidad externa versus calidad interna**.
Desde el punto de vista del usuario, el sistema 'funciona'. Pero desde el punto de vista del
mantenimiento, la estructura interna eleva drásticamente el costo del cambio.

En el diagnóstico inicial identificamos 9 debilidades técnicas principales:
1. **Long Method / Large Class:** El método `procesar` recibía 10 parámetros y ejecutaba 5 casos de uso.
2. **Primitive Obsession:** Estados y tipos de trámites representados por strings dispersos sin validación formal.
3. **Repeated Switch:** Condicionales en cascada para evaluar comandos y estados en múltiples lugares.
4. **Data Clumps:** Parámetros como asunto, detalle, tipo y prioridad viajaban siempre juntos sin encapsular.
5. **Divergent Change:** Modificar la estructura del JSON o agregar una regla de negocio obligaba a editar la misma clase.

Priorizamos corregir la fragilidad del modelo de dominio y el acoplamiento de la persistencia
antes de considerar extensiones funcionales."

---

## 04:00 a 06:30 Refactorings y principios SOLID (Fermín Alliot)

**Fermín Alliot:**  
"Para resolver esta deuda técnica aplicamos un proceso de refactoring seguro documentado en 5 pasos:
1. **Extract Method:** Aislamos las validaciones de invariantes y las reglas de transición.
2. **Move Method y Creación del Dominio:** Creamos `Solicitud` en `solicitudes/dominio.py` como una
   entidad inmutable (`@dataclass(frozen=True)`). Ahora es la propia entidad la que protege sus invariantes
   y resuelve las transiciones de estado mediante métodos puros como `asignar()` o `cambiar_estado()`.
3. **Introduce Parameter Object:** Introdujimos `NuevaSolicitud` y `FiltroSolicitudes` para agrupar
   datos cohesivos y eliminar la dispersión de parámetros.
4. **Enums de Dominio:** Centralizamos estados (`EstadoSolicitud`), tipos y prioridades para garantizar
   seguridad en tiempo de diseño.

Esto aplica directamente el principio de **Responsabilidad Única (SRP)**: el dominio conoce
únicamente las reglas del negocio y no sabe si se persiste en memoria o en disco."

---

## 06:30 a 09:00 Persistencia desacoplada y Suite de Pruebas (Gabriel Antuña)

**Gabriel Antuña:**  
"En la capa de persistencia aplicamos el principio de **Inversión de Dependencias (DIP)**:
`ModuloSolicitudes` no depende de archivos concretos, sino de la interfaz abstracta `RepositorioSolicitudes`.
Implementamos dos adaptadores: `RepositorioMemoria` (ideal para tests rápidos) y `RepositorioJson`
con escritura atómica mediante archivos temporales y reemplazo seguro, protegiendo los datos
ante fallos imprevistos.

Para verificar que ninguna refactorización alteró el comportamiento externo, construimos
una batería de **40 pruebas automatizadas** bajo el patrón Arrange-Act-Assert:
- Pruebas de caracterización que evalúan indistintamente la versión inicial y la refactorizada.
- Pruebas de matriz de estados que comprueban las 16 combinaciones posibles de transición.
- Pruebas de fallo simulado y archivos corruptos."

*(Ejecutar en vivo):*
```console
python -m unittest discover -s tests -v
python -m mypy
python -m ruff check .
```

"Vemos que las 40 pruebas pasan en verde y las comprobaciones de tipos estáticos y linter
confirman la integridad del sistema."

---

## 09:00 a 11:00 Code Review cruzado, Trazabilidad e IA (Ambos)

**Fermín Alliot:**  
"Llevamos a cabo un **Code Review profesional entre pares** utilizando un checklist de 8 dimensiones
(funcionalidad, diseño, errores, persistencia, contratos, etc.). Como revisores cruzados, analizamos
aspectos como la consistencia de nombres, la duplicación justificada en `__post_init__` y la
preservación absoluta del archivo `inicial.py`, lo cual verificamos mediante Git."

*(Ejecutar en consola):*
```console
git log --oneline --decorate
git diff estado-inicial estadorefactorizado -- solicitudes/inicial.py
```

**Gabriel Antuña:**  
"Respecto al uso de Inteligencia Artificial, encuadramos la experiencia bajo los contenidos
de la **Unidad 5 de la cátedra: 'La IA como Copiloto'**. Como equipo asumimos el rol de pilotos en
la arquitectura, programación y validación. La IA se empleó de manera complementaria para explorar
alternativas sintácticas de inmutabilidad, generar catálogos sintéticos y estructurar el checklist
de revisión técnica."

---

## 11:00 a 13:00 Conclusiones y cierre (Ambos)

**Fermín Alliot:**  
"Como conclusión técnica, este trabajo me demostró que el refactoring no consiste en reescribir
código por gusto estético, sino en transformaciones metódicas respaldadas por pruebas que reducen
el costo del cambio sin alterar el comportamiento. Encapsular la entidad de dominio permitió que el
sistema sea predecible y robusto."

**Gabriel Antuña:**  
"Por mi parte, destaco la importancia del desacoplamiento de capas y el uso de contratos. Poder
cambiar el motor de persistencia sin tocar las reglas de negocio demuestra el valor real de los
principios SOLID en proyectos profesionales. Como trabajo futuro, para un entorno productivo
quedaría incorporar concurrencia mediante base de datos relacional y autenticación de usuarios."

**Fermín Alliot:**  
"Muchas gracias por su atención y quedamos a disposición de la cátedra para responder cualquier pregunta."
