"""Vérification des réponses Python côté app : lance python_runner.py dans
un processus séparé, avec un délai maximal, et renvoie le résultat par cas
de test. Voir python_runner.py pour les règles de comparaison."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from python_runner import RESULT_MARKER

RUNNER = Path(__file__).parent / "python_runner.py"
TIMEOUT_SECONDS = 5


def run_tests(exercise_path: str, user_code: str, timeout: float = TIMEOUT_SECONDS) -> dict:
    """Exécute le code de l'utilisateur sur les cas de test de l'exercice.

    Renvoie un dict :
    - {"status": "ok", "results": [...]}  un résultat par cas de test ;
    - {"status": "error", "message": ...} code invalide, fonction absente ;
    - {"status": "timeout", "message": ...} délai dépassé (boucle infinie ?).
    """
    with tempfile.TemporaryDirectory() as work_dir:
        try:
            completed = subprocess.run(
                # -I : mode isolé (ni variables PYTHON*, ni site utilisateur).
                [sys.executable, "-I", str(RUNNER), str(Path(exercise_path).resolve())],
                input=user_code,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout,
                cwd=work_dir,  # un fichier écrit par erreur n'atterrit pas dans le projet
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "message": f"Délai de {timeout:g} s dépassé : boucle infinie, "
                "ou algorithme trop lent ?",
            }

    _, marker, payload = completed.stdout.rpartition(RESULT_MARKER)
    if not marker:
        return {
            "status": "error",
            "message": completed.stderr.strip()[-2000:]
            or "Le processus s'est arrêté sans renvoyer de résultat.",
        }
    return json.loads(payload)
