from abc import ABC, abstractmethod

class ManejadorDescargas(ABC):

    @abstractmethod
    def descargar_y_mover(
        self,
        click_descarga: callable,
        cedula: str,
        nombre: str,
        carpeta_destino: str
    ) -> str | None:
        pass
