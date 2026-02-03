import logging

from logic.context import PersonaContext
from logic.ports.alturas_portal import AlturasPortal
from logic.steps.result.step_result import StepResult
from logic.steps.step import Step


class BuscarPorCedula(Step):

    def __init__(self, portal: AlturasPortal):
        self.portal = portal
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: PersonaContext) -> StepResult:
        try:
            self.logger.info("Buscando cedula: %s", ctx.cedula)
            self.portal.buscar_cedula(ctx.cedula)
            return StepResult.SUCCESS
        except Exception as e:
            self.logger.error(e)
            return StepResult.FAILURE
