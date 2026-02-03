from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from infra import SeleniumAlturasPortal, CSVDocumentHandler, FileSystemDownloadHandler, FileSystemFolderHandler
from logic import GlobalContext
from logic.pipeline.base_pipeline_executor import BasePipelineExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from logic.pipeline.pipeline import Pipeline
from logic.steps import CargarPersonas, AbrirPortal, BuscarPorCedula, ObtenerCertificado, ObtenerFolder, \
    DescargarCertificado


def process_persona(persona):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=Options()
    )

    try:
        portal = SeleniumAlturasPortal(driver)

        pipeline = Pipeline([
            AbrirPortal(portal),
            BuscarPorCedula(portal),
            ObtenerCertificado(portal),
            ObtenerFolder(FileSystemFolderHandler("output/folder")),
            DescargarCertificado(
                portal,
                FileSystemDownloadHandler("downloads/")
            )
        ])

        pipeline.run(persona)

    finally:
        driver.quit()


class AlturasPipelineExecutor(BasePipelineExecutor):

    def __init__(self):
        self.alturasPortal = None
        self.driver = None

    def initialize_resources(self):
        # inicializamos el driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=Options()
        )
        # Inicializamos el portal
        self.alturasPortal = SeleniumAlturasPortal(self.driver)

    def load_global_context(self):
        # Cargamos las personas desde el CSV
        # Manejador de documentos
        manejadorDocumentos = CSVDocumentHandler()
        # Cargar personas
        cargarPersonas = CargarPersonas(manejadorDocumentos, "data/personas.csv")
        # Crear contexto global
        global_context = GlobalContext()
        cargarPersonas.run(global_context)
        return global_context

    def process_all_contexts(self, global_context):
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(process_persona, persona)
                for persona in global_context.personas
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error procesando persona: {e}")

