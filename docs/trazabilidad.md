# Matriz de trazabilidad

| Requisito de la consigna | Desarrollo o código | Evidencia de verificación |
|---|---|---|
| Sistema base con tres estructuras y cuatro operaciones como mínimo | catalogos.py, inicial.py, alcance.md | 13 pruebas iniciales y demo_inicial.txt |
| Calidad externa e interna | diagnostico.md | contrato funcional frente a D01 a D09 |
| Ocho debilidades con evidencia, ubicación, impacto, riesgo y prioridad | nueve filas en diagnostico.md | símbolos y líneas del tag estado-inicial |
| SOLID y Clean Code según corresponda | dominio.py, modulo.py, repositorios.py | tabla de principios en refactorings.md |
| Cuatro refactorings, incluidos los tres obligatorios | R01 a R05 en refactorings.md | diff estado-inicial frente a estadorefactorizado |
| Pruebas antes y después | tests/test_contrato.py y demás tests | suite_completa.txt y validacion.json |
| Code review aplicado y correcciones | code_review.md | observaciones CR01 a CR06, revisión por dos ejes |
| Conclusiones y límites | informe.md y refactorings.md | reflexión técnica sin métricas inventadas |
| README, /docs y commits claros | README.md y árbol Git | git log y tags |
| Tags de estados y de etapas | historial Git | estado-inicial, estadorefactorizado, etapa-diagnostico, etapa-refactoring, etapa-pruebas, etapa-docs |
| Declaración y evidencia de IA | docs/ia/registro.md y revision_agentes.md | cuatro actividades resumidas, pedidos reales y resultados de revisión |
| Fundamentación de decisiones | referencias_tecnicas.md e informe.md | Fowler, Clean Code y SOLID vinculados con cambios y pruebas |
| PDF único y anexo ZIP | entrega/ | generación, revisión visual y comprobación del paquete |
| Video de 10 a 15 minutos con cámara inicial y voz propia | guion_video.md | Guion preparado; grabación y enlace pendientes |
| Repositorio GitHub y enlaces accesibles | config_entrega.json y publicacion.md | GitHub público verificado; enlace del video pendiente |

Los tags señalan hitos del proceso, no ocho entregas independientes. El tag
estado-inicial conserva el ejecutable original; el tag estadorefactorizado
se fija sobre el cierre técnico. etapa-docs identifica la documentación final.

## Correspondencia entre diagnóstico y cambios

| Debilidad | Transformación | Casos de prueba que protegen el cambio |
|---|---|---|
| D01, D06 | R01 validación expresiva | registro válido e inválido |
| D01, D05, D07 | R02 transición dentro de Solicitud | ciclo, matriz, responsable, salto y reapertura |
| D02 | R03 objetos de parámetros | registro y filtros combinados |
| D04, D05 | R04 repositorios | contrato común, inexistentes y persistencia |
| D03, D07, D08 | R05 enums e inmutabilidad | filtros inválidos, entidad original y colección independiente |
| D09 | Mejora de robustez adicional | fallo de reemplazo y archivo corrupto |

No todas las debilidades equivalen a un bug. R01 a R05 reorganizan diseño;
las garantías adicionales de persistencia se verifican con pruebas específicas.
