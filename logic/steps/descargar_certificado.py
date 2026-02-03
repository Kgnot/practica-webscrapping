import logging
from logic.context import PersonaContext
from logic.ports.alturas_portal import AlturasPortal
from logic.ports.manejador_descargas import ManejadorDescargas
from logic.steps import Step
from logic.steps.result.step_result import StepResult


class DescargarCertificado(Step):

    def __init__(self, portal: AlturasPortal, manejador_descargas: ManejadorDescargas):
        self.portal = portal
        self.manejador_descargas = manejador_descargas
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: PersonaContext) -> StepResult:
        if ctx.certificado is None:
            return StepResult.FAILURE

        destino = self.manejador_descargas.descargar_y_mover(
            click_descarga=lambda: self.portal.click_descarga(ctx.certificado),
            cedula=ctx.cedula,
            nombre=ctx.nombre,
            carpeta_destino=ctx.folder_persona
        )

        if destino is None:
            # ctx.errors.append("Error descargando certificado")
            self.logger.error("No se ha podido descargar el certificado.")
            # ctx.stop = True
            return StepResult.FAILURE

        ctx.download_path = destino
        return StepResult.SUCCESS
