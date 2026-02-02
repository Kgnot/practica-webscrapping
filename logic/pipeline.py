import logging

from logic import BotContext
from logic.steps.step import Step


class Pipeline:
    def __init__(self, steps: list[Step]):
        self.steps = steps
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, ctx: BotContext) -> None:
        self.logger.info("Iniciando pipeline")

        for step in self.steps:
            if ctx.stop:
                self.logger.info("Pipeline detenido por contexto")
                break
            self.logger.info(f"Ejecutando step: {step.__class__.__name__}")
            step.run(ctx)
