from logic.ports.alturas_portal import AlturasPortal
from logic.steps.step import Step


class AbrirPortal(Step):

    def __init__(self, portal: AlturasPortal):
        self.portal = portal

    def run(self, ctx):
        self.portal.abrir()
