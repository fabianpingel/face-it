"""
Test 1: Stimmt die Umgebung?

Prueft die Dinge, an denen die Einrichtung am haeufigsten scheitert -
falsche Python-Version, falsches OpenCV-Paket, fehlendes numpy.
"""

import sys

import pytest


def test_python_version():
    """Der Workshop braucht Python 3.10 bis 3.12 (siehe pyproject.toml)."""
    assert sys.version_info >= (3, 10), (
        f"Python {sys.version_info.major}.{sys.version_info.minor} ist zu alt. "
        "Gebraucht wird 3.10 oder neuer."
    )
    assert sys.version_info < (3, 13), (
        f"Python {sys.version_info.major}.{sys.version_info.minor} ist zu neu. "
        "opencv-contrib-python gibt es dafuer noch nicht als Fertigpaket."
    )


def test_numpy_vorhanden():
    numpy = pytest.importorskip("numpy", reason="numpy fehlt - uv sync ausfuehren")
    assert numpy.__version__ >= "1.26", (
        f"numpy {numpy.__version__} ist zu alt, gebraucht wird 1.26 oder neuer."
    )


def test_opencv_vorhanden():
    cv2 = pytest.importorskip("cv2", reason="OpenCV fehlt - uv sync ausfuehren")
    assert cv2.__version__.startswith("4."), (
        f"OpenCV {cv2.__version__} ist die falsche Hauptversion. Gebraucht wird 4.x - "
        "in OpenCV 5 fehlen die Haar-Cascades, die Station 3 fuer den Vergleich "
        "2001 gegen 2023 braucht."
    )


def test_opencv_ist_die_contrib_variante():
    """
    Station 3b braucht cv2.face, das nur in opencv-contrib-python steckt.
    Wer versehentlich das schlanke opencv-python installiert hat, merkt es
    sonst erst im Workshop.
    """
    import cv2

    assert hasattr(cv2, "face"), (
        "cv2.face fehlt - es ist das schlanke opencv-python installiert, nicht "
        "opencv-contrib-python. Beide gleichzeitig geht nicht. Reparatur:\n"
        "  uv pip uninstall opencv-python\n"
        "  uv sync"
    )


def test_haar_cascade_liegt_bei():
    """Station 3 vergleicht Haar-Cascade (2001) gegen YuNet (2023)."""
    import cv2
    from pathlib import Path

    datei = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    assert datei.is_file(), f"Haar-Cascade nicht gefunden unter {datei}"

    erkenner = cv2.CascadeClassifier(str(datei))
    assert not erkenner.empty(), "Die Haar-Cascade laesst sich nicht laden."


def test_faceit_importierbar(fc):
    """Das gemeinsame Hilfsmodul muss sich laden lassen."""
    assert fc.TESTMODUS is True, (
        "FACEIT_TEST ist nicht gesetzt - die Tests wuerden Fenster oeffnen."
    )


def test_daten_ordner_ist_umgelenkt(fc):
    """
    Sicherung: Die Tests duerfen nie im echten data/-Ordner arbeiten,
    weil 99_cleanup.py im Testmodus ohne Rueckfrage loescht.
    """
    assert fc.DATEN.name == "_testlauf", (
        f"Der data-Ordner zeigt auf {fc.DATEN} statt auf data/_testlauf. "
        "FACEIT_DATEN wurde nicht gesetzt - Tests abgebrochen, bevor Daten "
        "verloren gehen."
    )
