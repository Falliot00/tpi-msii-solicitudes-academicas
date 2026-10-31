import unittest
from dataclasses import FrozenInstanceError, replace

from solicitudes.dominio import Estado, Prioridad, Solicitud, TipoSolicitud


class ReglasDeEstado(unittest.TestCase):
    def solicitud(self, estado: Estado = Estado.ABIERTA, responsable: int | None = 1) -> Solicitud:
        return Solicitud(
            1, 1, "Certificado", "", TipoSolicitud.CONSTANCIA, Prioridad.ALTA, estado, responsable
        )

    def test_matriz_completa_de_transiciones(self) -> None:
        permitidos = {
            Estado.ABIERTA: {Estado.ABIERTA, Estado.EN_PROCESO, Estado.CANCELADA},
            Estado.EN_PROCESO: {Estado.EN_PROCESO, Estado.RESUELTA, Estado.CANCELADA},
            Estado.RESUELTA: {Estado.RESUELTA},
            Estado.CANCELADA: {Estado.CANCELADA},
        }
        for origen in Estado:
            for destino in Estado:
                with self.subTest(origen=origen, destino=destino):
                    actual = self.solicitud(origen)
                    if destino in permitidos[origen]:
                        self.assertEqual(actual.cambiar_estado(destino).estado, destino)
                    else:
                        with self.assertRaises(ValueError):
                            actual.cambiar_estado(destino)

    def test_no_se_muta_la_entidad_original(self) -> None:
        actual = self.solicitud(responsable=None)
        asignada = actual.asignar(2)
        self.assertIsNone(actual.responsable_id)
        self.assertEqual(asignada.responsable_id, 2)
        with self.assertRaises(FrozenInstanceError):
            setattr(actual, "estado", Estado.RESUELTA)

    def test_construccion_rechaza_invariantes_invalidas(self) -> None:
        valida = self.solicitud(responsable=None)
        for datos in [
            {"id": 0},
            {"id": -1},
            {"id": True},
            {"estudiante_id": 99},
            {"estudiante_id": True},
            {"asunto": " "},
            {"responsable_id": 99},
            {"responsable_id": True},
            {"estado": Estado.RESUELTA},
            {"estado": Estado.EN_PROCESO},
        ]:
            with self.subTest(datos=datos):
                with self.assertRaises(ValueError):
                    replace(valida, **datos)
