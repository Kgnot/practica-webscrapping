from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistroAlturas:
    programa: str
    fecha: datetime
    boton: any # Después miramos como reemplazar 'any'