from pathlib import Path
import json


class GestionLangue:
    """Gestion de la langue de l'application (lecture / écriture)."""

    def __init__(self, fichier_config: Path):
        self.fichier_config = fichier_config

    def lire(self) -> str:
        """lire la langue - fichier JSON"""
        try:
            with open(self.fichier_config, "r", encoding="utf-8") as f:
                return json.load(f).get("langueSelectionnee", "fr")
        except (FileNotFoundError, json.JSONDecodeError):
            return "fr"

    def ecrire(self, code_langue: str) -> None:
        """Écrit le code langue dans le fichier."""
        with open(self.fichier_config, "w", encoding="utf-8") as f:
            json.dump(
                {"langueSelectionnee": code_langue},
                f,
                indent=4,
                ensure_ascii=False
            )