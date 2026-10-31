# Alcance y criterios de aceptación

Fuente normativa: TP MS2V2.pdf, páginas 1 a 6, cátedra de Metodología de Sistemas II.
El modelo PPTX, la guía DOCX y su README son orientativos. Este documento registra
las decisiones del prototipo, sin convertir los ejemplos del modelo en requisitos.

## Caso y autor

Gestión de solicitudes académicas. Único integrante: Fermin Alliot, legajo 101414,
comisión M25 C4-02. Carrera Tecnicatura Universitaria en Programación a Distancia.
Se construye un prototipo educativo nuevo con asistencia de IA y se conserva
su estado inicial antes de modificar su estructura. Las verificaciones y la
revisión técnica asistida se identifican en sus evidencias.

## Funcionalidad observable

1. Registrar una solicitud de un estudiante del catálogo, con asunto no vacío,
   detalle opcional, tipo y prioridad válidos. Normalizar espacios exteriores.
2. Asignar o reasignar un responsable del catálogo mientras esté abierta o en proceso.
3. Cambiar estado. Abierta permite en_proceso o cancelada; en_proceso permite
   resuelta o cancelada; los estados finales no permiten volver a otros estados.
   Repetir el mismo estado es idempotente. Entrar en proceso requiere responsable.
4. Consultar por estado, tipo, prioridad y coincidencia parcial del asunto sin
   distinguir mayúsculas. Los filtros se combinan mediante AND; se conserva el
   orden de registro. Búsqueda vacía significa no filtrar. No se eliminan tildes.
5. Reportar total y cantidades por cada uno de los cuatro estados, aun con cero casos.

Se utiliza memoria estructurada o JSON local. Entidades: Estudiante, Responsable
y Solicitud. Tipos: constancia, equivalencia e inscripcion. Prioridades: baja,
media y alta. No se implementan autenticación, servidor, frontend, concurrencia,
correo, adjuntos ni administración de catálogos. Los datos son sintéticos.

## Aceptación técnica y documental

- Conservar la versión inicial y verificar las mismas reglas en la versión final.
- Diagnosticar al menos ocho debilidades con ubicación, evidencia, impacto,
  riesgo y prioridad. Distinguir smells de fallos observados.
- Documentar Extract Method, Move Method/reubicación, Introduce Parameter Object
  y al menos una transformación adicional. Justificar SOLID según corresponda.
- Registrar pruebas de éxito, rechazo y borde; ejecutar typecheck y lint.
- Aplicar un checklist de code review con observaciones y correcciones.
- Producir informe PDF, anexo ZIP, repositorio local recuperable y guion para
  grabar con voz propia. Publicación GitHub y grabación requieren acciones posteriores.
- Crear tags estado-inicial, estadorefactorizado, etapa-diagnostico,
  etapa-refactoring, etapa-pruebas y etapa-docs con hitos reales, sin retrofechar.
- Declarar herramienta, finalidad y grado de intervención de IA y adjuntar
  intercambios relevantes. No atribuir al estudiante una defensa aún no realizada.

## Referencias de la materia utilizadas

- SEMANA_1_CALIDAD.pdf, unidad 1, especialmente páginas 4 y 5: deuda y smells.
- SEMANA_II_SOLID.pdf, unidad 1: responsabilidades y dependencia de abstracciones.
- SEMANA_III_CLEAN_CODE.pdf, unidad 1, páginas 3 y 4: refactoring, review y TAC.
- Semana 2.pdf, unidad 3, páginas 1 y 5: AAA y regresión.
- MdS II UNIDAD 4 Semana 1.pdf: commits, objetos y tags de Git.

Las conclusiones sobre este prototipo se fundamentan en su código y evidencias,
no en afirmaciones generales de que una herramienta garantiza ausencia de fallos.
