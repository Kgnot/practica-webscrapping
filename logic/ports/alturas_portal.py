from abc import ABC, abstractmethod

from logic.models.registro_alturas import RegistroAlturas


class AlturasPortal(ABC):

    @abstractmethod
    def abrir(self): pass

    @abstractmethod
    def buscar_cedula(self, cedula: str): pass

    @abstractmethod
    def obtener_registros(self) -> list[RegistroAlturas] | None: pass

    @abstractmethod
    def click_descarga(self, registro:RegistroAlturas): pass
