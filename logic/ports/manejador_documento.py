from abc import ABC, abstractmethod


class ManejadorDocumento(ABC):

    @abstractmethod
    def cargar(self, ruta_documento: str):
        pass

    @abstractmethod
    def filtrar_validos(self):
        pass

    @abstractmethod
    def obtener_lista_documentos(self) -> list | None:
        pass
