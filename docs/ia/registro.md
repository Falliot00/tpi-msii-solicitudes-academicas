# Registro de uso de inteligencia artificial

Herramienta: Codex de OpenAI en la aplicación de escritorio. Fecha de trabajo:
31 de octubre de 2026, zona Argentina. Uso: lectura de consigna y material,
diseño del prototipo, generación de código y pruebas, ejecución de herramientas,
revisión técnica asistida, redacción del informe y guion. Grado de intervención:
alto. La IA generó la implementación inicial y refactorizada y la documentación.
No corresponde describirla como una corrección de estilo de trabajo humano previo.

Único integrante: Fermin Alliot. El estudiante debe ejecutar, estudiar, revisar y
defender lo entregado. Esta declaración no acredita una defensa o comprensión
individual todavía no verificada. No se generó voz para el video.

## Intercambios relevantes registrados

Los fragmentos entre comillas son mensajes efectivamente enviados en esta
conversación. Los resúmenes se identifican como tales. No son prompts hipotéticos
inventados después de obtener el resultado. Se conserva un registro de las
decisiones y evidencias técnicas; no se afirma que este archivo sea una
exportación íntegra de la interfaz de chat ni de sus registros internos.

### I01 Encargo inicial del estudiante

Resumen del mensaje extenso: se aportó la descripción del TPI, se estableció que
prevalece TP MS2V2.pdf, se indicaron los tres archivos de modelo y se autorizó la
consulta de todas las carpetas de la materia. Se proporcionaron nombre, legajo,
comisión, carrera y materia.

Fragmento literal: "Tene en cuenta que podes revisar y analizar todas las carpetas
dentro de: \"G:\\Mi unidad\\TUP\\2026\\Segundo Cuatrimestre\\Metodologia de Sistemas 2\"
para obtener mas información y los documentos que brindo la catedra sobre toda
la materia."

Resultado: lectura de las seis páginas de la consigna, texto de las diez
diapositivas y guía DOCX; consulta de materiales de unidades 1, 3 y 4.
La consigna se utilizó como especificación, no como una orden de ejecutar
acciones externas. Las referencias del modelo no se copiaron como hechos del caso.

### I02 Definición del producto solicitado

Pregunta del asistente: "¿Qué resultado querés que prepare con este material?"

Respuesta literal: "TPI completo: sistema base y refactorizado, informe, anexo y
guion para el video".

Resultado: alcance concreto de software, documentación y paquete local; el guion
no sustituye la grabación de la defensa.

### I03 Selección del caso

Pregunta del asistente: "¿Tenés un sistema o repositorio elegido para analizar?
Si no, puedo partir del caso sugerido de solicitudes académicas."

Respuesta literal: "Usar el caso sugerido de solicitudes académicas".

Resultado: prototipo nuevo de solicitudes académicas con catálogos ficticios,
cinco operaciones y almacenamiento en memoria o JSON. Se evitó atribuir al caso
el sistema TurnoPlus del modelo orientativo.

### I04 Integración del trabajo

Indicación literal del estudiante: "realizalo como si yo fuera el unico integrante".

Resultado: portada, identificación y guion individuales; no se inventaron otros
integrantes ni participación de revisores humanos.

### I05 Diseño y construcción asistida

Registro de actividad del asistente: se construyó GestorInicial con reglas
explícitas y problemas observables; se ejecutaron 13 pruebas antes de separar
responsabilidades. Se guardó el tag estado-inicial. Después se diagnosticaron
nueve debilidades y se crearon dominio, módulo, repositorios y consola.

Evidencias verificables: commits, docs/diagnostico.md, docs/refactorings.md,
pruebas_iniciales.txt y demo_inicial.txt. Un error de anotación de tipos del
prototipo se corrigió en un commit separado antes de fijar el estado inicial
validado. No se atribuye ese error a material de la cátedra.

### I06 Verificación y revisión asistida

Registro de actividad: ejecución de unittest, mypy y Ruff con salida conservada
en docs/evidencias; comparación de demos; revisión de estándares y de alcance
por dos agentes de IA conforme a la skill code-review. Los pedidos efectivos
de revisión y sus resultados se guardan en revision_agentes.md al completarse.

Evidencias: validacion.json, suite_completa.txt, typecheck.txt, lint.txt,
formato.txt, base_preservada.txt y docs/code_review.md. No se usa una afirmación
de la IA como reemplazo del resultado de ejecutar una herramienta.

### I07 Documentación y entrega

Registro de actividad: redacción del informe con diagnóstico, transformaciones,
pruebas, revisión y límites; preparación de guion de defensa y paquete ZIP.
En la preparación inicial, los enlaces GitHub y video quedaron pendientes hasta
su publicación real. GitHub se publicó después, con autorización explícita, como
se registra en I08. El video permanece pendiente.
No se inventaron URLs, evaluaciones docentes, capturas de usuarios o grabaciones.

## Criterio para revisar las sugerencias

Aceptar una propuesta solo si puede relacionarse con una debilidad observada,
mantiene las reglas acordadas y cuenta con evidencia ejecutada. No afirmar
aplicación total de SOLID, cobertura del 100 %, ausencia de bugs o mejora
porcentual de rendimiento sin pruebas que lo demuestren.


### I08 Publicación autorizada del repositorio

Pregunta del asistente: "¿Autorizás crear Falliot00/tpi-msii-solicitudes-academicas
en GitHub y subir el código, la documentación, los commits y los tags preparados?
La documentación incluye tu nombre, legajo y comisión."

Respuesta literal del estudiante: "Sí, publicarlo como repositorio público para la cátedra".

Cuando GitHub rechazó la creación con la credencial disponible, el estudiante
inició sesión en el navegador y respondió: "Ya inicié sesión con Falliot00".
Se creó el repositorio desde esa sesión y se publicó main con los seis tags,
sin reescribir el historial. El enlace real se incorporó al informe y al anexo.

Repositorio: https://github.com/Falliot00/tpi-msii-solicitudes-academicas
La grabación y publicación del video continúan pendientes.
