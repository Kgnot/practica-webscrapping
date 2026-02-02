from dataclasses import dataclass, field
from typing import List
from logic.context.persona_context import PersonaContext

@dataclass
class GlobalContext:
    personas: List[PersonaContext] = field(default_factory=list)
    stop: bool = False
    errors: List[str] = field(default_factory=list)