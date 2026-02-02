from typing import Optional

from logic import BotContext
from logic.ports.manejador_folder import ManejadorFolder
from logic.steps.step import Step


class ObtenerFolder(Step):

    def __init__(self, manejador_folder: ManejadorFolder):
        self.manejador_folder = manejador_folder

    def run(self, ctx: BotContext):
        folder: Optional[str] = self.manejador_folder.obtener_folder_persona(ctx.nombre)

        if folder is None:
            ctx.stop = True
            ctx.errors.append(
                f"No existe carpeta para la persona: {ctx.nombre}"
            )
            return

        ctx.folder_persona = folder
