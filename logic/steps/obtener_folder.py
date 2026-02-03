from typing import Optional

from logic.context import PersonaContext
from logic.ports.manejador_folder import ManejadorFolder
from logic.steps.result.step_result import StepResult
from logic.steps.step import Step


class ObtenerFolder(Step):

    def __init__(self, manejador_folder: ManejadorFolder):
        self.manejador_folder = manejador_folder

    def run(self, ctx: PersonaContext) -> StepResult:
        folder: Optional[str] = self.manejador_folder.obtener_folder_persona(ctx.nombre)

        if folder is None:
            return StepResult.FAILURE

        ctx.folder_persona = folder
        return StepResult.SUCCESS
