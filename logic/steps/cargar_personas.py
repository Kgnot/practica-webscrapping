from logic import BotContext
from logic.ports.manejador_documento import ManejadorDocumento
from logic.steps.step import Step


class CargarPersonas(Step):
    def __init__(self, manejador: ManejadorDocumento, ruta: str):
        self.manejador = manejador
        self.ruta = ruta

    def run(self, ctx : BotContext):
        self.manejador.cargar(self.ruta)
        self.manejador.filtrar_validos()
        ctx.personas = self.manejador.obtener_lista_documentos()
