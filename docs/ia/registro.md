# Anexo de metodología y herramientas de asistencia

Este anexo da cumplimiento a los puntos 6.1 y 7 de la consigna oficial del TPI:
declaración de herramientas utilizadas, finalidad, grado de intervención y registro
ordenado de las interacciones de soporte.

| Herramienta | Finalidad / Uso | Fecha | Grado de intervención |
|---|---|---|---|
| Asistente de IA (OpenAI / ChatGPT) | Consultas conceptuales de refactoring, generación de catálogos sintéticos, co-revisión de checklist y soporte de redacción | 31/10/2026 | Bajo (Copiloto / Asistencia complementaria) |
| Herramientas de análisis estático (Mypy, Ruff) | Verificación de tipado estático, conformidad PEP 8 y detección automática de problemas de estilo | 31/10/2026 | Automatizado (Linter / Typechecker) |

## Modalidad de trabajo y autoría del equipo

El trabajo práctico integrador fue realizado en modalidad grupal por:
- **Fermín Alliot** · Legajo 101414 · Comisión M25 C4-02
- **Gabriel Antuña** · Legajo 100506 · Comisión M25 C4-12

Bajo el marco conceptual de la cátedra (**Unidad 5: La IA como Copiloto**), los integrantes
asumieron el rol de **pilotos** en la toma de decisiones, diseño de la arquitectura,
programación del sistema base con deuda técnica, refactorización segura y construcción
de las pruebas unitarias. La inteligencia artificial actuó exclusivamente como **copiloto**
para contrastar alternativas técnicas y optimizar la comunicación de resultados.

### Distribución de responsabilidades del equipo:
- **Fermín Alliot:** Análisis del caso y reglas de negocio, diseño y refactoring del modelo
  de dominio inmutable (`dominio.py`), pruebas de caracterización y de contrato (`test_dominio.py`, `test_contrato.py`).
- **Gabriel Antuña:** Arquitectura de persistencia desacoplada (`repositorios.py`, `modulo.py`),
  interfaz por línea de comandos (`cli.py`), tests de integración/persistencia y pipeline de validación estática.
- **Responsabilidad compartida:** Inspección y Code Review cruzado con checklist técnico,
  diagnóstico de code smells, consolidación de la documentación técnica y defensa en video.

## Registro ordenado de intercambios con IA (Copiloto)

| ID | Consulta / Prompt del equipo | Objetivo técnico | Resultado obtenido y criterio de aplicación |
|---|---|---|---|
| P01 | "¿Qué alternativas existen en Python para modelar entidades de dominio inmutables asegurando integridad y compatibilidad con JSON?" | Contrastar `@dataclass(frozen=True)` vs NamedTuple vs clases con atributos protegidos. | Se seleccionó `@dataclass(frozen=True)` con `__post_init__` para validar invariantes al instanciar. |
| P02 | "Sugerir una estructura de datos sintéticos anonimizados para un caso educativo de solicitudes académicas (estudiantes, coordinadores y tipos de trámites)." | Generar catálogos ficticios sin datos personales reales para cumplir con la pauta de privacidad de la cátedra. | Se incorporaron los catálogos en memoria en `catalogos.py` con 3 estudiantes y 3 responsables. |
| P03 | "Basado en Martin Fowler (Refactoring) y Clean Code, ¿qué preguntas clave estructuran un checklist de code review para refactoring seguro y preservación de contratos?" | Diseñar el checklist técnico para la revisión cruzada de código. | Se estructuraron los 8 ejes del checklist en `docs/code_review.md` (funcionalidad, diseño, errores, contratos, etc.). |
| P04 | "¿Cómo estructurar un script en Python con ReportLab para generar un informe técnico profesional en PDF con tablas y diagrama de bloques?" | Resolver dudas sobre estilos de párrafo, anchos de tabla y flujo de elementos de ReportLab. | Implementación del script `tools/construir_informe.py` para generar el entregable PDF formal. |
| P05 | "Revisar la redacción del guion de defensa para asegurar claridad, precisión conceptual y cumplimiento del límite de tiempo (10-15 minutos)." | Optimizar los tiempos y transiciones de habla entre ambos integrantes. | Estructuración equilibrada de la exposición grupal en `docs/guion_video.md`. |

## Validación y control de calidad por el equipo

Ninguna propuesta o fragmento generado por IA se incorporó sin una revisión crítica
previa, adaptación al contexto del problema y verificación mediante pruebas de software:

1. **Pruebas automatizadas:** La suite de 40 tests unitarios y de contrato (`unittest`)
   garantiza que el sistema refactorizado mantiene el 100% de la funcionalidad observable.
2. **Análisis estático:** `mypy` certifica ausencia de inconsistencias de tipos y `ruff`
   garantiza el apego a los estándares PEP 8.
3. **Validación manual:** Ambos integrantes ejecutaron y auditaron manualmente los escenarios
   de borde (estados inválidos, fallos de disco, archivos corruptos), registrados en `docs/evidencias/validacion_manual.md`.

La defensa del proyecto se realiza en video grabado con cámara encendida y voz propia de ambos integrantes.
