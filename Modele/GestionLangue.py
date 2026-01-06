from pathlib import Path
import json


class GestionLangue:
    """Gestion de la langue de l'application (lecture / écriture)."""

    def __init__(self, fichier_config: Path):
        self.fichier_config = fichier_config

    def lire(self) -> str:
        """Retourne le code langue ('fr', 'en', 'es', 'br')."""
        if not self.fichier_config.exists():
            return "fr"

        with open(self.fichier_config, "r", encoding="utf-8") as f:
            return json.load(f).get("langueSelectionnee", "fr")

    def ecrire(self, code_langue: str) -> None:
        """Écrit le code langue dans le fichier."""
        with open(self.fichier_config, "w", encoding="utf-8") as f:
            json.dump(
                {"langueSelectionnee": code_langue},
                f,
                indent=4,
                ensure_ascii=False
            )

