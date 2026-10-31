# Solicitudes académicas

Prototipo educativo para el TPI de Metodología de Sistemas II de Fermin Alliot,
legajo 101414, comisión M25 C4-02. Carrera Tecnicatura Universitaria en Programación
a Distancia. Datos operativos ficticios.

## Estado inicial

Python 3.11 o superior. Sin dependencias para ejecutar el sistema y sus pruebas.

```console
python -m solicitudes
python -m unittest discover -s tests -v
```

El sistema registra solicitudes, asigna responsables, cambia estados, filtra
y genera un reporte por estado. Contiene Estudiante, Responsable y Solicitud
(esta última representada por diccionario). Puede almacenar datos en memoria
o archivo JSON. La estructura inicial concentra reglas, consultas y persistencia.

Este prototipo fue construido para la actividad con asistencia de IA. No se
presenta como un sistema previo de producción ni como experiencia laboral real.
