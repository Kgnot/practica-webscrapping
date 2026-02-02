import logging

from logic.context import PersonaContext
from logic.ports.alturas_portal import AlturasPortal
from logic.steps.step import Step


class ObtenerCedula(Step):

    def __init__(self, portal: AlturasPortal):
        self.portal = portal
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: PersonaContext):
        try:
            self.logger.info("Buscando cedula: %s", ctx.cedula)
            self.portal.buscar_cedula(ctx.cedula)
        except Exception as e:
            self.logger.error(e)
            ctx.stop = True
