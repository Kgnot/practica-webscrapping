from pathlib import Path

from logic.ports.manejador_folder import ManejadorFolder


class FileSystemFolderHandler(ManejadorFolder):

    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)

    def obtener_folder_persona(self, nombre: str) -> Path | None:
        # Vamos a la dirección de la carpeta
        folder = self.base_path / nombre

        #Si el folder existe devolvemos el folder
        if folder.exists() and folder.is_dir():
            return folder

        return None
