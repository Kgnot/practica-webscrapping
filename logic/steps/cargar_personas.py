from logic.context.global_context import GlobalContext
from logic.context.persona_context import PersonaContext
from logic.ports.manejador_documento import ManejadorDocumento
from logic.steps.result.step_result import StepResult
from logic.steps.step import Step


class CargarPersonas(Step):
    def __init__(self, manejador: ManejadorDocumento, ruta: str):
        self.manejador = manejador
        self.ruta = ruta

    def run(self, ctx: GlobalContext) -> StepResult:
        self.manejador.cargar(self.ruta)
        self.manejador.filtrar_validos()
        ctx.personas = [
            PersonaContext(
                cedula=registro["DOCUMENTO"],
                nombre=registro["NOMBRE"].strip().upper()
            )
            for registro in self.manejador.obtener_lista_documentos()
        ]
        return StepResult.SUCCESS  # TODO: manejar errores
