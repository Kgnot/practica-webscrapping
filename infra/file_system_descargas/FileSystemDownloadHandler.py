import os
import time

from logic.ports.manejador_descargas import ManejadorDescargas


class FileSystemDownloadHandler(ManejadorDescargas):

    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder

    def descargar_y_mover(self, click_descarga, cedula, nombre, carpeta_destino):
        before = set(os.listdir(self.temp_folder))
        click_descarga()

        for _ in range(30):
            time.sleep(1)
            after = set(os.listdir(self.temp_folder))
            diff = after - before
            valid = [f for f in diff if not f.endswith(".crdownload")]

            if valid:
                filename = valid[0]
                origen = os.path.join(self.temp_folder, filename)
                destino = os.path.join(
                    carpeta_destino,
                    f"{cedula}_ALTURAS{os.path.splitext(filename)[1]}"
                )
                os.replace(origen, destino)
                return destino

        return None
