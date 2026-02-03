from logic.ports.alturas_portal import AlturasPortal
from logic.steps.result.step_result import StepResult
from logic.steps.step import Step


class AbrirPortal(Step):

    def __init__(self, portal: AlturasPortal):
        self.portal = portal

    def run(self, ctx) -> StepResult:
        self.portal.abrir()
        # TODO: Manejar errores al abrir el portal
        return StepResult.SUCCESS
