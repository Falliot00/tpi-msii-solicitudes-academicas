# Solicitudes académicas

Prototipo educativo para el TPI de Metodología de Sistemas II de Fermin Alliot,
legajo 101414, comisión M25 C4-02. Carrera Tecnicatura Universitaria en Programación
a Distancia. Datos operativos ficticios.

## Ejecución y uso

Python 3.11 o superior. Sin dependencias para ejecutar el sistema y sus pruebas.

```console
python -m solicitudes demo
python -m solicitudes --implementacion inicial demo
python -m solicitudes catalogos
python -m solicitudes --help
python -m unittest discover -s tests -v
```

Las demos utilizan memoria y no modifican archivos. Los demás comandos usan
datos/solicitudes.json o una ruta elegida con --archivo antes del comando.
Para repetir el ejemplo con ID 1, usar una ruta nueva:

```console
python -m solicitudes --archivo datos/ejemplo.json registrar --estudiante 1 --asunto "Constancia para beca" --detalle "Ciclo 2026" --tipo constancia --prioridad alta
python -m solicitudes --archivo datos/ejemplo.json asignar 1 1
python -m solicitudes --archivo datos/ejemplo.json estado 1 en_proceso
python -m solicitudes --archivo datos/ejemplo.json listar --estado en_proceso --prioridad alta --texto beca
python -m solicitudes --archivo datos/ejemplo.json estado 1 resuelta
python -m solicitudes --archivo datos/ejemplo.json reporte
```

Tomar el ID devuelto por registrar si ya existían datos. Para usar la versión
base con la consola actual, agregar --implementacion inicial antes del comando.
El tag estado-inicial conserva el ejecutable original, que se demostraba con
python -m solicitudes sin subcomando.

Abierta permite pasar a en_proceso (requiere responsable) o cancelada. En proceso
permite resuelta o cancelada. Los estados finales no admiten cambios ni
reasignación. Repetir un estado es idempotente. Los filtros se combinan con AND;
el texto busca parte del asunto sin distinguir mayúsculas ni eliminar tildes.
Salida JSON por stdout. Errores de dominio: código 2; de persistencia: código 3.
El archivo JSON no admite edición concurrente segura.

## Validación

```console
python -m pip install -r requirements-dev.txt
python tools/verificar.py
```

El verificador conserva resultados de unittest, mypy estricto sobre la aplicación,
Ruff lint, formato, preservación de inicial.py y comparación de demos. Usa las
versiones fijadas en requirements-dev.txt. La suite contiene 39 métodos: los
mismos 13 casos para cada versión, dos de dominio, seis de repositorios y cinco
de consola. Los subcasos no se cuentan como tests independientes.

Validado con Windows y Python 3.12.14; Python 3.11 no se ejecutó por separado.
No se midió cobertura. No hay React/Next.js, por lo que React Doctor no corresponde.
Los resultados finales están en docs/evidencias/validacion.json.

## Historial y documentación

```console
git log --oneline --decorate
git tag --list
git diff estado-inicial estadorefactorizado -- solicitudes
git show estado-inicial:solicitudes/inicial.py
```

Tags: estado-inicial, estadorefactorizado, etapa-diagnostico, etapa-refactoring,
etapa-pruebas y etapa-docs. El nombre estadorefactorizado reproduce la consigna.
El archivo inicial permanece idéntico en la versión final.

docs contiene alcance, diagnóstico de nueve debilidades, cinco refactorings,
checklist de revisión, trazabilidad, informe editable, guion de defensa y registro
de IA. Los resultados reales de herramientas se conservan en docs/evidencias.

El ZIP incluye Repositorio.bundle con commits y tags. Para recuperarlo desde
el ZIP extraído:

```console
git clone Repositorio.bundle solicitudes-academicas
```

La carpeta codigo del ZIP se puede ejecutar sin Git. El bundle conserva el
historial. No se hizo push ni se publicó el repositorio automáticamente.

## Informe y entrega

```console
python -m pip install -r requirements-documentacion.txt
python tools/construir_informe.py
python tools/empaquetar.py
```

El informe se guarda en entrega/Alliot_Fermin_TPI_MSII.pdf. Para empaquetar,
primero completar el cierre de Git. entrega/ está excluida del versionado para
evitar archivos recursivos y contenido dependiente de su propio commit.

Completar las URLs reales en config_entrega.json y regenerar PDF y ZIP antes
de entregar. GitHub y video figuran pendientes mientras no se publiquen. La
cátedra exige PDF, repositorio, ZIP y video cargados. El guion de 12 a 14 minutos
no sustituye grabar con cámara al inicio y voz propia.

Este prototipo fue construido para la actividad con asistencia de IA. No se
presenta como un sistema previo de producción ni como experiencia laboral real.
