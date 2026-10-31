import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solicitudes.dominio import Estado, Prioridad, Solicitud, TipoSolicitud
from solicitudes.repositorios import ErrorPersistencia, RepositorioJson, RepositorioMemoria


def ejemplo(identificador: int = 1) -> Solicitud:
    return Solicitud(
        identificador, 1, "Constancia", "Beca", TipoSolicitud.CONSTANCIA, Prioridad.MEDIA
    )


class ContratoRepositorio:
    def verificar(self, repositorio: RepositorioMemoria | RepositorioJson) -> None:
        assert repositorio.listar() == []
        repositorio.guardar(ejemplo(2))
        repositorio.guardar(ejemplo(1))
        assert [s.id for s in repositorio.listar()] == [1, 2]
        repositorio.guardar(ejemplo(1).asignar(1).cambiar_estado(Estado.EN_PROCESO))
        assert repositorio.obtener(1).estado == Estado.EN_PROCESO
        assert len(repositorio.listar()) == 2
        lista = repositorio.listar()
        lista.clear()
        assert len(repositorio.listar()) == 2
        with self.assertRaisesRegex(ValueError, "Solicitud inexistente"):
            repositorio.obtener(99)


class MemoriaTest(ContratoRepositorio, unittest.TestCase):
    def test_contrato_de_almacenamiento(self) -> None:
        self.verificar(RepositorioMemoria())


class JsonTest(ContratoRepositorio, unittest.TestCase):
    def setUp(self) -> None:
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.archivo = Path(self.temporal.name) / "solicitudes.json"
        self.repositorio = RepositorioJson(self.archivo)

    def test_contrato_de_almacenamiento(self) -> None:
        self.verificar(self.repositorio)

    def test_reabrir_y_recuperar_acentos(self) -> None:
        solicitud = Solicitud(
            1, 1, "Inscripción", "Año próximo", TipoSolicitud.INSCRIPCION, Prioridad.ALTA
        )
        self.repositorio.guardar(solicitud)
        self.assertEqual(RepositorioJson(self.archivo).obtener(1), solicitud)

    def test_archivo_corrupto_no_se_sobrescribe(self) -> None:
        self.archivo.write_text("{incompleto", encoding="utf-8")
        with self.assertRaises(ErrorPersistencia):
            self.repositorio.guardar(ejemplo())
        self.assertEqual(self.archivo.read_text(encoding="utf-8"), "{incompleto")

    def test_rechaza_formatos_e_invariantes_invalidos(self) -> None:
        registro = ejemplo().a_registro()
        casos = [
            None,
            {},
            [None],
            [dict(registro, id=True)],
            [dict(registro, id=0)],
            [dict(registro, estudiante_id=99)],
            [dict(registro, asunto=" ")],
            [dict(registro, responsable_id=99)],
            [dict(registro, tipo="otro")],
            [dict(registro, estado="resuelta")],
            [registro, registro],
        ]
        for datos in casos:
            with self.subTest(datos=datos):
                self.archivo.write_text(json.dumps(datos), encoding="utf-8")
                with self.assertRaises(ErrorPersistencia):
                    self.repositorio.listar()

    def test_fallo_de_reemplazo_preserva_archivo_y_limpia_temporal(self) -> None:
        self.repositorio.guardar(ejemplo())
        original = self.archivo.read_bytes()
        with patch("solicitudes.repositorios.os.replace", side_effect=OSError("Disco")):
            with self.assertRaisesRegex(ErrorPersistencia, "No se pudo guardar"):
                self.repositorio.guardar(ejemplo(2))
        self.assertEqual(self.archivo.read_bytes(), original)
        self.assertEqual(list(self.archivo.parent.glob("solicitudes-*.tmp")), [])
