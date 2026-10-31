"""Crear anexo con código versionado, PDF, historial Git y hashes verificables."""

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def git(*argumentos: str) -> bytes:
    return subprocess.check_output(["git", *argumentos], cwd=RAIZ)


def main() -> None:
    if git("status", "--porcelain").strip():
        raise SystemExit("Hay cambios sin commit: completar el cierre antes de empaquetar")
    pdf = RAIZ / "entrega" / "Alliot_Fermin_TPI_MSII.pdf"
    if not pdf.exists():
        raise SystemExit("Generar primero el informe PDF")
    bundle = RAIZ / "entrega" / "Repositorio.bundle"
    git("bundle", "create", str(bundle), "--all")
    git("bundle", "verify", str(bundle))
    archivos = git("ls-files", "-z").decode("utf-8").split("\0")
    contenido = {"codigo/" + nombre: (RAIZ / nombre).read_bytes() for nombre in archivos if nombre}
    contenido["Repositorio.bundle"] = bundle.read_bytes()
    contenido["Alliot_Fermin_TPI_MSII.pdf"] = pdf.read_bytes()
    contenido["Guion_video.md"] = (RAIZ / "docs" / "guion_video.md").read_bytes()
    contenido["LEER_PRIMERO.txt"] = (
        "TPI de Fermin Alliot. Código ejecutable en codigo/.\n"
        "Historial: git clone Repositorio.bundle solicitudes-academicas\n"
        "Completar GitHub y grabar el video con voz propia antes de entregar.\n"
        "El informe conserva explícitamente los enlaces pendientes.\n"
    ).encode("utf-8")
    hashes = {nombre: hashlib.sha256(datos).hexdigest() for nombre, datos in contenido.items()}
    contenido["MANIFEST_SHA256.json"] = json.dumps(hashes, indent=2, ensure_ascii=False).encode(
        "utf-8"
    )
    salida = RAIZ / "entrega" / "Anexo_Alliot_Fermin_TPI_MSII.zip"
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as archivo:
        for nombre, datos in contenido.items():
            archivo.writestr(nombre, datos)
    with zipfile.ZipFile(salida) as archivo:
        if archivo.testzip() is not None:
            raise SystemExit("El ZIP no superó su control de integridad")
        for nombre, esperado in hashes.items():
            if hashlib.sha256(archivo.read(nombre)).hexdigest() != esperado:
                raise SystemExit("Hash incorrecto: " + nombre)
    print("ZIP e integridad SHA-256: PASS")
    print(salida)


if __name__ == "__main__":
    main()
