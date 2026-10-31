# Refactorings aplicados y decisiones de diseño

Comparación estable: solicitudes/inicial.py en estado-inicial frente a los
módulos nuevos. La copia inicial permanece idéntica en el estado final.

## R01 Extract Method

Antes, procesar validaba estudiante y asunto dentro de su rama de registro:

```python
if estudiante_id not in [e.id for e in ESTUDIANTES]:
    raise ValueError("Estudiante inexistente")
if not asunto.strip():
    raise ValueError("El asunto es obligatorio")
```

Después, dominio.validar_estudiante_y_asunto expresa esa regla y se utiliza
desde NuevaSolicitud.validar y desde_textos. La conversión de entrada conserva
la precedencia de los mensajes de error. La regla deja de estar mezclada con
persistencia, IDs y reporte. Atiende D01 y D06. Verificación:
test_registros_invalidos_no_se_guardan en ambas versiones.

## R02 Move Method y reubicación de responsabilidad

Antes, GestorInicial.procesar consultaba s["estado"], armaba p y cambiaba el
diccionario. Después, Solicitud.cambiar_estado consulta TRANSICIONES y devuelve
una nueva entidad. ModuloSolicitudes obtiene, solicita el cambio y guarda.

```python
actual = self._repositorio.obtener(solicitud_id)
solicitud = actual.cambiar_estado(convertir_enum(Estado, estado, "Estado inválido"))
self._repositorio.guardar(solicitud)
```

La regla queda junto al estado al que protege. No se añade una nueva transición.
Atienden D01, D05 y D07. Verificación: test_matriz_completa_de_transiciones
recorre los 16 pares de estados; el contrato compartido prueba falta de
responsable, saltos, reapertura, idempotencia y cierre.

## R03 Introduce Parameter Object

Antes, procesar recibía diez argumentos además de self y combinaba campos de
registro, consulta y cambios de estado. Después, registrar recibe NuevaSolicitud
con los cinco datos de alta; buscar recibe FiltroSolicitudes con cuatro filtros.

```python
def registrar(self, nueva: NuevaSolicitud) -> Solicitud:
    nueva.validar()
```

Los argumentos dejan de depender de una cadena accion. La CLI continúa
aceptando texto y lo transforma al vocabulario del dominio. Atiende D02.
Verificación: test_registro_y_normalizacion y test_filtros_combinados_y_busqueda.

## R04 Extract Class e inversión de dependencia

Antes, GestorInicial creaba directorios y escribía JSON en _guardar. Después,
RepositorioSolicitudes define listar, obtener y guardar. RepositorioMemoria y
RepositorioJson satisfacen esa interfaz; ModuloSolicitudes recibe uno al
construirse. No conoce rutas, codificación ni escritura en disco.

Se justifica la interfaz porque hay dos adaptadores utilizados: memoria para
demo y pruebas, JSON para uso persistente. No se agregan interfaces de futuras
bases de datos. La búsqueda por ID se centraliza; el adaptador JSON compone el
adaptador de memoria para reutilizar reemplazo y orden. Atiende D04 y D05.
Verificación: el mismo contrato de repositorio se aplica a ambos adaptadores.

La escritura temporal con os.replace y la validación del archivo son mejoras
de robustez adicionales para D09. No se presentan como refactorings puros,
porque agregan comportamiento ante archivos dañados o fallos de disco.

## R05 Reemplazar representaciones primitivas y encapsular la colección

Antes, estados/tipos/prioridades eran literales repetidos y los diccionarios
almacenados se devolvían por referencia. Después, Estado, TipoSolicitud y
Prioridad son enums; Solicitud es una dataclass frozen. a_registro genera un
diccionario independiente para JSON. listar devuelve una colección nueva.
Atienden D03, D07 y D08. Verificación: test_no_se_muta_la_entidad_original,
contrato de repositorio y test_archivo_inicial_es_compatible_con_version_final.

## SOLID y Clean Code

| Principio | Aplicación y alcance |
|---|---|
| SRP | Dominio concentra invariantes; módulo coordina operaciones; repositorios almacenan; CLI interpreta entradas y presenta resultados |
| OCP | Cambiar entre los dos almacenamientos no modifica las reglas del módulo. Agregar estados sí requiere revisar reglas y pruebas; no se promete extensibilidad ilimitada |
| LSP | Los dos adaptadores son sustituibles para el contrato declarado de listar/obtener/guardar; se prueba igualdad de reglas y excepciones de ausencia. JSON además puede fallar por I/O, documentado en la CLI |
| ISP | El contrato de almacenamiento contiene solo tres operaciones que el módulo utiliza. No se fuerza una jerarquía de interfaces para cada método |
| DIP | ModuloSolicitudes depende de RepositorioSolicitudes (Protocol), no de la clase JSON |

Clean Code se concreta en nombres expresivos, operaciones separadas, filtros
cohesivos y errores controlados. Las excepciones de dominio usan ValueError;
ErrorPersistencia identifica fallos de almacenamiento. No se capturan todas las
excepciones con un bloque que simule éxito.

## Límites de las decisiones

El almacenamiento JSON reescribe el conjunto y usa búsqueda lineal al leer;
es suficiente para pocos datos locales. El cálculo max(id)+1 y os.replace no
resuelven concurrencia entre procesos. El reemplazo atómico protege ante fallo
de reemplazo, no equivale a una transacción de base de datos ni a una garantía
de durabilidad frente a corte de energía. No hay autenticación ni autorización.
