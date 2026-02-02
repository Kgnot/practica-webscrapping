from dataclasses import dataclass
from typing import Optional

from logic.models.registro_alturas import RegistroAlturas


@dataclass
class BotContext:
    cedula: str = ""
    nombre: str = ""
    certificado: RegistroAlturas | None = None
    folder_persona: Optional[str] = None
    download_path: str | None = None
    stop: bool = False
    errors: list[str] | None = list[str]
