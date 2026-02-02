from pathlib import Path
import logging

import pandas as pd
import time


from logic.ports.manejador_documento import ManejadorDocumento


class CSVDocumentHandler(ManejadorDocumento):

    def __init__(self, retries: int = 5, delay: int = 10):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.retries = retries
        self.delay = delay
        self._df = None

    def cargar(self, ruta_documento: str):
        intentos = 0
        path = Path(ruta_documento)

        self.logger.info(f"Cargando archivo {path}")

        while intentos < self.retries:
            try:
                self._df = pd.read_csv(path)
                self._df.columns = self._df.columns.str.strip()
                return
            except FileNotFoundError:
                intentos += 1
                time.sleep(self.delay)

        raise FileNotFoundError(f"No se pudo cargar el archivo: {ruta_documento}")

    def filtrar_validos(self):
        if self._df is None:
            raise RuntimeError("Documento no cargado")

        mask = pd.to_numeric(
            self._df["DOCUMENTO"], errors="coerce"
        ).notnull()

        self._df = self._df[mask]


    def obtener_lista_documentos(self) -> list:
        if self._df is None:
            raise RuntimeError("Documento no cargado")

        return (
            self._df[["DOCUMENTO", "NOMBRE"]]
            .to_dict(orient="records")
        )
