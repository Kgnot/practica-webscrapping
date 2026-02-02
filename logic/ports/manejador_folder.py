from abc import ABC, abstractmethod
from pathlib import Path


class ManejadorFolder(ABC):

    @abstractmethod
    def obtener_folder_persona(self, nombre: str) -> Path | None:
        pass
