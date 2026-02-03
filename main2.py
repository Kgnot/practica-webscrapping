import pandas as pd
import time
import os
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


# Carga de CSV

class PersonLoader:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load(self):
        intentos = 0
        max_intentos = 5

        while intentos < max_intentos:
            try:
                # Rezar para que lea el archivo
                df = pd.read_csv(self.csv_path)
                df.columns = df.columns.str.strip()

                # Filtrar documentos válidos
                df_validos = df[pd.to_numeric(df["DOCUMENTO"], errors="coerce").notnull()]
                print("Archivo CSV cargado exitosamente.")
                return df_validos[["DOCUMENTO", "NOMBRE"]].to_dict("records")

            except FileNotFoundError:
                intentos += 1
                print(f"ADVERTENCIA: Archivo se está cargando... (Intento {intentos}/{max_intentos})")
                print("   Verifica que Google Drive esté abierto y sincronizando.")

                if intentos < max_intentos:
                    time.sleep(10)  # Timer de reintento
                else:
                    print("\nERROR CRÍTICO: No se pudo encontrar el archivo 'datos_rpa.csv'.")
                    print("Asegúrate de haber ejecutado el AppScript primero y que la unidad G: esté activa.")
                    input("Presiona Enter para cerrar...")
                    sys.exit()
            except Exception as e:
                print(f"Error inesperado al leer el CSV: {e}")
                sys.exit()


# Entrar al link, cambiar el desplegable a cédula e ingresar el documento

class AlturasPortal:
    URL = "https://app2.mintrabajo.gov.co/CentrosEntrenamiento/consulta_ext.aspx"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def search_by_cedula(self, cedula):
        dropdown = self.wait.until(
            EC.presence_of_element_located((By.ID, "contenido_tipo_documentoTextBox"))
        )
        Select(dropdown).select_by_value("CC")

        campo = self.wait.until(
            EC.visibility_of_element_located((By.ID, "contenido_valor_consulta"))
        )
        campo.clear()
        campo.send_keys(cedula)

        try:
            self.driver.find_element(By.ID, "contenido_btn_consultar").click()
        except:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Consultar']"))
            )
            btn.click()

    def wait_for_results(self):
        self.wait.until(
            EC.presence_of_element_located((By.ID, "contenido_GridView2"))
        )


# Recorrer la tabla y hacer la comparación de fechas

class RecordsTable:
    def __init__(self, driver):
        self.driver = driver

    def get_latest_alturas_certificate(self):
        filas = self.driver.find_elements(
            By.XPATH, "//table[@id='contenido_GridView2']//tr[td]"
        )

        fecha_max = datetime.min
        boton_objetivo = None

        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            programa = celdas[0].text.strip().upper()
            texto_fecha = celdas[4].text.strip()

            if "TRABAJO EN ALTURAS" not in programa:
                continue

            try:
                fecha = datetime.strptime(texto_fecha, "%d/%m/%Y")
            except:
                continue

            if fecha > fecha_max:
                fecha_max = fecha
                boton_objetivo = celdas[-1].find_element(By.TAG_NAME, "a")

        if boton_objetivo:
            return fecha_max, boton_objetivo

        return None


# Meter los PDF en un temp para luego pasarlos a las carpetas individuales

class Downloader:
    def __init__(self, base_folder):
        self.base_folder = base_folder

    def get_person_folder(self, nombre):
        folder = os.path.join(self.base_folder, nombre)

        # Verificar que el AppScritp sirva para algo
        if not os.path.exists(folder):
            print(f"   ⚠️ ERROR: No existe la carpeta '{nombre}' en G:. ¿Sincronización pendiente?")
            return None
        return folder

    def wait_new_file(self, before_files, temp_folder, timeout=25):
        for _ in range(timeout):
            time.sleep(1)
            after_files = set(os.listdir(temp_folder))
            diff = after_files - before_files
            valid = [f for f in diff if not f.endswith(".crdownload")]
            if valid:
                return valid[0]
        return None

    def move_and_rename(self, filename, temp_folder, cedula, nombre):
        ext = os.path.splitext(filename)[1]
        final_name = f"{cedula}_ALTURAS{ext}"
        origen = os.path.join(temp_folder, filename)

        carpeta_persona = self.get_person_folder(nombre)
        if carpeta_persona is None:
            return None

        destino = os.path.join(carpeta_persona, final_name)
        if os.path.exists(destino):
            os.remove(destino)

        os.rename(origen, destino)
        return destino


# Proceso completo

class AlturasBot:
    def __init__(self, portal, downloader, temp_folder):
        self.portal = portal
        self.downloader = downloader
        self.temp_folder = temp_folder

    def process_person(self, cedula, nombre):
        print(f"\nProcesando a {nombre} de cédula {cedula}")
        self.portal.open()

        try:
            self.portal.search_by_cedula(cedula)
        except Exception as e:
            print(f"Error formulario: {e}")
            return

        try:
            self.portal.wait_for_results()
        except:
            print("No hay registros en el portal.")
            return

        table = RecordsTable(self.portal.driver)
        result = table.get_latest_alturas_certificate()

        if not result:
            print(" No existe certificado Alturas.")
            return

        fecha, boton = result
        print(f"Certificado más reciente encontrado: {fecha.date()}")

        before = set(os.listdir(self.temp_folder))
        boton.click()
        print("Descargando archivo...")

        file = self.downloader.wait_new_file(before, self.temp_folder)
        if not file:
            print("Descarga fallida (Timeout).")
            return

        destino = self.downloader.move_and_rename(file, self.temp_folder, cedula, nombre)
        if destino:
            print("Archivo guardado exitosamente")
        else:
            print(" No se pudo mover el archivo: Carpeta de destino no encontrada.")


# Correr cosas
def main():
    import time
    from datetime import datetime
    import os

    # ===== MEDICIÓN DE TIEMPO =====
    inicio_ts = time.time()
    inicio_humano = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print(f"🚀 Proceso iniciado: {inicio_humano}")
    print("=" * 60)

    # ===== RUTAS =====
    ruta_csv = "data/personas.csv"
    ruta_temp = "downloads/"
    ruta_entrenamiento = "entrenamiento/"

    if not os.path.exists(ruta_temp):
        os.makedirs(ruta_temp)

    # ===== CARGA DE PERSONAS =====
    loader = PersonLoader(ruta_csv)
    registros = loader.load()

    print(f"👥 Se cargaron {len(registros)} personas para procesar.")

    # ===== CONFIGURACIÓN SELENIUM =====
    chrome_options = Options()
    prefs = {
        "download.default_directory": ruta_temp,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    portal = AlturasPortal(driver)
    downloader = Downloader(ruta_entrenamiento)
    bot = AlturasBot(portal, downloader, ruta_temp)

    # ===== PROCESO PRINCIPAL =====
    try:
        for i, persona in enumerate(registros, start=1):
            print(f"\n--- [{i}/{len(registros)}] ------------------------------")

            cedula = str(int(persona["DOCUMENTO"]))
            nombre = str(persona["NOMBRE"]).strip().upper()

            bot.process_person(cedula, nombre)

    finally:
        driver.quit()

        # ===== FIN Y TIEMPOS =====
        fin_ts = time.time()
        fin_humano = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duracion = fin_ts - inicio_ts

        minutos = int(duracion // 60)
        segundos = int(duracion % 60)

        print("\n" + "=" * 60)
        print(f"🏁 Proceso finalizado: {fin_humano}")
        print(f"⏱️  Duración total: {minutos} min {segundos} seg")
        print("=" * 60)


if __name__ == "__main__":
    main()
