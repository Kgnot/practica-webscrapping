from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logic.ports.alturas_portal import AlturasPortal
from logic.models.registro_alturas import RegistroAlturas


class SeleniumAlturasPortal(AlturasPortal):
    _URL = "https://app2.mintrabajo.gov.co/CentrosEntrenamiento/consulta_ext.aspx"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def abrir(self):
        self.driver.get(self._URL)

    def buscar_cedula(self, cedula: str):
        # Seleccionamos el tipo de documento
        dropdown = self.wait.until(
            EC.presence_of_element_located((By.ID, "contenido_tipo_documentoTextBox"))
        )
        Select(dropdown).select_by_value("CC")
        # Rellenamos el campo
        campo = self.wait.until(
            EC.presence_of_element_located((By.ID, "contenido_valor_consulta"))
        )
        campo.clear()
        campo.send_keys(cedula)
        # Buscamos el elemento
        self.driver.find_element(By.ID, "contenido_consultar").click()

    def obtener_registros(self) -> list[RegistroAlturas]:
        try:
            self.wait.until(
                EC.presence_of_element_located((By.ID, "contenido_GridView2"))
            )
        except TimeoutException:
            return []

        filas = self.driver.find_elements(
            By.XPATH, "//table[@id='contenido_GridView2']//tr[td]"
        )

        registros = []

        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")

            programa = celdas[0].text.strip().upper()
            texto_fecha = celdas[4].text.strip()

            try:
                fecha = datetime.strptime(texto_fecha, "%d/%m/%Y")
            except ValueError:
                continue

            boton = celdas[-1].find_element(By.TAG_NAME, "a")

            registros.append(
                RegistroAlturas(
                    programa=programa,
                    fecha=fecha,
                    boton=boton
                )
            )

        return registros

    def click_descarga(self, registro: RegistroAlturas):
        registro.boton.click()
