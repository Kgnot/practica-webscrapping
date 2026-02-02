import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from infra import SeleniumAlturasPortal, CSVDocumentHandler, FileSystemFolderHandler, FileSystemDownloadHandler
from logic import BotContext
from logic.pipeline import Pipeline
from logic.steps import AbrirPortal, CargarPersonas, ObtenerCedula, ObtenerCertificado, ObtenerFolder, \
    DescargarCertificado, Step


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Inicio de programa:

logger.info("Iniciando configuración de recursos externos")

# Definimos recursos externos
chrome_options = Options()
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
# Definimos recursos que usan los pasos [Puertos]

alturasPortal = SeleniumAlturasPortal(driver)
manejadorDocumentos = CSVDocumentHandler()
manejadorFolder = FileSystemFolderHandler("C:/Users/enamo/Desktop/certificados_alturas/")
manejadorDescargas = FileSystemDownloadHandler("C:/Users/enamo/Downloads/")

# definimos cada uno de los pasos a usar en el pipeline
abrirPortal = AbrirPortal(alturasPortal)
cargarPersonas = CargarPersonas(manejadorDocumentos,
                                "data/personas.csv")  # Aqui podemos añadir la ruta o en la clase con enums
obtenerCedula = ObtenerCedula(alturasPortal)
obtenerCertificado = ObtenerCertificado(alturasPortal)
obtenerFolder = ObtenerFolder(manejadorFolder)
descargarCertificado = DescargarCertificado(alturasPortal, manejadorDescargas)

steps: list[Step] = [
    abrirPortal,
    cargarPersonas,
    obtenerCedula,
    obtenerCertificado,
    obtenerFolder,
]
# ahora definimos el contexto de la aplicación y el pipeline
botContext: BotContext = BotContext()

logger.info("Iniciando pipeline de obtención de certificados de alturas")

pipeline: Pipeline = Pipeline(steps)

pipeline.run(botContext)
