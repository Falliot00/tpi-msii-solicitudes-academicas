"""Entrada ejecutable del sistema base."""

import json

from solicitudes.inicial import GestorInicial


def main() -> None:
    gestor = GestorInicial()
    solicitud = gestor.procesar(
        "registrar",
        estudiante_id=1,
        asunto="Certificado regular",
        detalle="Para beca",
        tipo="constancia",
        prioridad="alta",
    )
    gestor.procesar("asignar", solicitud_id=solicitud["id"], responsable_id=1)
    gestor.procesar("estado", solicitud_id=solicitud["id"], estado="en_proceso")
    print(json.dumps(gestor.procesar("listar"), ensure_ascii=False, indent=2))
    print(json.dumps(gestor.procesar("reporte"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
