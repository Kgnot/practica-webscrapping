from logic.context import GlobalContext, PersonaContext
from logic.models.registro_alturas import RegistroAlturas
from logic.ports.alturas_portal import AlturasPortal
from logic.steps.step import Step


class ObtenerCertificado(Step):

    def __init__(self, alturas_portal: AlturasPortal):
        self.alturas_portal = alturas_portal

    def run(self, ctx: PersonaContext):
        # Obtenemos los certificados desde el portal
        registrosAlturas: list[RegistroAlturas] | None = self.alturas_portal.obtener_registros()

        if not registrosAlturas:
            ctx.certificado = None
            ctx.stop = True
            return

        alturas = [
            r for r in registrosAlturas
            if "TRABAJO EN ALTURAS" in r.programa.upper()
        ]
        ultimo_registro: RegistroAlturas = max(alturas, key=lambda r: r.fecha)
        # Ingresamos el certificado al contexto
        ctx.certificado = ultimo_registro
