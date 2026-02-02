import logging

from logic.context import PersonaContext
from logic.steps.step import Step


class Pipeline:
    def __init__(self, steps: list[Step]):
        self.steps = steps
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: PersonaContext) -> None:
        self.logger.info("Iniciando pipeline")
        for step in self.steps:
            self.logger.info(f"Ejecutando step: {step.__class__.__name__}")
            step.run(ctx)
