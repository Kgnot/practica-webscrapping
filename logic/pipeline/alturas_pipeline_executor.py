from infra import SeleniumAlturasPortal, CSVDocumentHandler, FileSystemDownloadHandler, FileSystemFolderHandler
from logic import GlobalContext
from logic.pipeline.base_pipeline_executor import BasePipelineExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from logic.pipeline.pipeline import Pipeline
from logic.steps import CargarPersonas, AbrirPortal, ObtenerCedula, ObtenerCertificado, ObtenerFolder, \
    DescargarCertificado


class AlturasPipelineExecutor(BasePipelineExecutor):

    def __init__(self):
        self.alturasPortal = None
        self.driver = None

    def initialize_resources(self):
        # Código movido aquí desde el main
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=Options()
        )
        self.alturasPortal = SeleniumAlturasPortal(self.driver)

    def load_global_context(self):
        # Cargo personas desde el CSV
        manejadorDocumentos = CSVDocumentHandler()
        cargarPersonas = CargarPersonas(manejadorDocumentos, "data/personas.csv")
        global_context = GlobalContext()
        cargarPersonas.run(global_context)
        return global_context

    def process_all_contexts(self, global_context):
        pipeline = Pipeline([
            AbrirPortal(self.alturasPortal),
            ObtenerCedula(self.alturasPortal),
            ObtenerCertificado(self.alturasPortal),
            ObtenerFolder(FileSystemFolderHandler("output/folder")),
            DescargarCertificado(self.alturasPortal, FileSystemDownloadHandler("downloads/"))
        ])

        for persona in global_context.personas:
            pipeline.run(persona)
