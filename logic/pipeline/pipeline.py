import logging

from logic.context import PersonaContext
from logic.steps.result.step_result import StepResult
from logic.steps.step import Step


class Pipeline:
    def __init__(self, steps: list[Step]):
        self.steps = steps
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: PersonaContext) -> None:
        self.logger.info("Iniciando pipeline")
        for step in self.steps:
            self.logger.info(f"Ejecutando step: {step.__class__.__name__}")
            result = step.run(ctx)
            if result == StepResult.FAILURE:
                self.logger.error(f"Pipeline abortado debido a fallo en: {step.__class__.__name__}")
                break  # Abortamos este contexto.
            if result == StepResult.SKIP:
                self.logger.warning(f"Pipeline detenido. Step {step.__class__.__name__} no encontró datos relevantes.")
                break  # Detenemos este contexto.
        self.logger.info(f"Pipeline finalizado para {ctx.nombre}")
