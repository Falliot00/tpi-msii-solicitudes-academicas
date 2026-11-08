# Validación técnica del equipo

Ejecutores: Fermín Alliot y Gabriel Antuña. Fecha: 31 de octubre de 2026.
Equipo: Windows 11, Python 3.14.6. Versión evaluada: tag estadorefactorizado (commit 58a18e4).

Estas comprobaciones fueron ejecutadas en entorno local por los integrantes para validar
la suite completa, las reglas de invariantes y la robustez ante fallos de persistencia.

Preparación, en PowerShell desde la raíz del repositorio:

```console
python --version
git rev-parse --short HEAD
python -m pip install -r requirements-dev.txt
mkdir docs\evidencias\manual
```

## V1 Suite completa

```console
python -m unittest discover -s tests -v 2>&1 | Out-File -Encoding utf8 docs\evidencias\manual\suite.txt
```

Esperado: "Ran 40 tests" y "OK" al final del archivo.
Resultado: PASS. Se ejecutaron las 40 pruebas en 0.045s sin fallos ni errores.

## V2 Transición de estado inválida

Una solicitud abierta no puede pasar directamente a resuelta.

```console
python -m solicitudes --archivo datos\validacion.json registrar --estudiante 1 --asunto "Prueba manual" --tipo constancia --prioridad alta
python -m solicitudes --archivo datos\validacion.json estado 1 resuelta
$LASTEXITCODE
```

Esperado: {"error": "Transición de estado no permitida"} y código 2.
Regla: TRANSICIONES en dominio.py y Solicitud.cambiar_estado.
Resultado: PASS. Salida: `{"error": "Transición de estado no permitida"}`, código de salida 2.

## V3 Pasar a en proceso sin responsable

```console
python -m solicitudes --archivo datos\validacion.json estado 1 en_proceso
$LASTEXITCODE
```

Esperado: {"error": "Debe asignarse un responsable"} y código 2.
Luego asignar y repetir: `asignar 1 1` y `estado 1 en_proceso` deben responder
con la solicitud en estado en_proceso y código 0.
Resultado: PASS. Rechazado inicialmente con código 2; tras asignar responsable ID 1, la transición fue aceptada con código 0.

## V4 Archivo JSON dañado

```console
Set-Content datos\roto.json "{roto"
python -m solicitudes --archivo datos\roto.json listar
$LASTEXITCODE
```

Esperado: {"error": "No se pudo leer el archivo de solicitudes"} y código 3,
sin que el archivo se sobrescriba.
Resultado: PASS. Salida: `{"error": "No se pudo leer el archivo de solicitudes"}`, código de salida 3. El archivo dañado se preservó íntegro.

## V5 Tipos, lint, formato y base preservada

```console
python -m mypy 2>&1 | Out-File -Encoding utf8 docs\evidencias\manual\mypy.txt
python -m ruff check . 2>&1 | Out-File -Encoding utf8 docs\evidencias\manual\ruff.txt
python -m ruff format --check . 2>&1 | Out-File -Encoding utf8 docs\evidencias\manual\formato.txt
git diff estado-inicial estadorefactorizado -- solicitudes/inicial.py
```

Esperado: mypy "Success", Ruff "All checks passed!", formato sin archivos a
reformatear y diff vacío.
Resultado: PASS. Mypy reportó "Success: no issues found in 8 source files". Ruff reportó "All checks passed!". Formato al 100%. Diff de `inicial.py` vacío (código 0).

## Observaciones

Todos los escenarios de prueba manual arrojaron exactamente los resultados esperados,
confirmando la preservación del comportamiento externo y la robustez del manejo de errores
y de persistencia en la versión refactorizada.

Al terminar las pruebas se eliminaron los archivos temporales de prueba `datos\validacion.json`
y `datos\roto.json`.
