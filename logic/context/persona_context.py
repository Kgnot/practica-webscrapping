from dataclasses import dataclass
from typing import Optional
from logic.models.registro_alturas import RegistroAlturas

@dataclass
class PersonaContext:
    cedula: str = ""
    nombre: str = ""
    certificado: Optional[RegistroAlturas] = None
    folder_persona: Optional[str] = None
    download_path: Optional[str] = None