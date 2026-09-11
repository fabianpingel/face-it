"""
Gemeinsame Einrichtung fuer alle Tests.

Die Tests pruefen, ob ein Rechner fuer den Workshop bereit ist. Sie laufen
komplett ohne Bildschirm und ohne Webcam:

  FACEIT_TEST    schaltet die Fenster ab (Bilder gehen nach data/_test/)
  FACEIT_KAMERA  ersetzt die Webcam durch ein gespeichertes Portrait
  FACEIT_DATEN   lenkt den data-Ordner in ein temporaeres Verzeichnis um

Der letzte Punkt ist wichtig: 99_cleanup.py loescht im Testmodus ohne
Rueckfrage. Ohne Umlenkung wuerden die Tests die Aufnahmen einer Klasse
vernichten.

Aufruf:
    uv run --extra tests pytest
"""

import os
import sys
from pathlib import Path

import pytest

PROJEKT = Path(__file__).resolve().parent.parent
CODE = PROJEKT / "code"
BEISPIELE = PROJEKT / "data" / "beispiele"

# code/ auf den Suchpfad, damit "import faceit" funktioniert - genauso wie
# beim Start eines Stationsskripts mit "uv run code/01_pixel.py".
sys.path.insert(0, str(CODE))


def pytest_configure(config):
    """Setzt den Testmodus, bevor faceit importiert wird."""
    os.environ["FACEIT_TEST"] = "1"
    # data/ in einen eigenen Unterordner umlenken. Nicht in das System-Temp,
    # damit die Lehrkraft nach einem Fehlschlag noch hineinsehen kann.
    ziel = PROJEKT / "data" / "_testlauf"
    ziel.mkdir(parents=True, exist_ok=True)
    os.environ["FACEIT_DATEN"] = str(ziel)


@pytest.fixture(scope="session")
def portraits():
    """Die freien Beispielportraits, nach Dateiname sortiert."""
    gefunden = sorted(BEISPIELE.glob("portrait_*.jpg"))
    if len(gefunden) < 2:
        pytest.skip(
            "Weniger als zwei Beispielportraits in data/beispiele/ - "
            "nachladen mit: uv run code/tools/portraits_holen.py"
        )
    return gefunden


@pytest.fixture(scope="session")
def fc():
    """Das Hilfsmodul faceit, im Testmodus geladen."""
    import faceit
    return faceit


@pytest.fixture(scope="session")
def detektor(fc):
    """Der YuNet-Gesichtsfinder."""
    return fc.detektor_laden()


@pytest.fixture(scope="session")
def erkenner(fc):
    """Das SFace-Modell, das aus einem Gesicht 128 Zahlen macht."""
    return fc.erkenner_laden()


def zahlen_aus_portrait(fc, detektor, erkenner, pfad):
    """
    Hilfsfunktion: Bild laden, ein Gesicht finden, 128 Zahlen berechnen.
    Gibt None zurueck, wenn kein Gesicht gefunden wurde.
    """
    import cv2

    bild = cv2.imread(str(pfad))
    assert bild is not None, f"Bild laesst sich nicht laden: {pfad}"
    gesichter = fc.gesichter_finden(detektor, bild)
    if not gesichter:
        return None
    groesstes = max(gesichter, key=lambda g: g[2] * g[3])
    return fc.gesicht_zu_zahlen(erkenner, bild, groesstes)
