"""
Test 2: Sind die Modelle da und laden sie?

Die beiden ONNX-Dateien liegen im Repository. Wenn ein Download abgebrochen
wurde, ist die Datei da, aber zu klein - dann laedt OpenCV sie nicht, und die
Fehlermeldung ist schwer zu deuten. Deshalb wird beides geprueft.
"""

import pytest


# Erwartete Groessen in Byte, mit Toleranz nach unten.
# yunet ist winzig, sface ist das 37-MB-Modell.
MINDESTGROESSE = {
    "yunet.onnx": 200_000,
    "sface.onnx": 30_000_000,
}


def test_modellordner_vorhanden(fc):
    assert fc.MODELLE.is_dir(), (
        f"Der Ordner {fc.MODELLE} fehlt. Nachladen mit:\n"
        "  uv run code/tools/modelle_holen.py"
    )


@pytest.mark.parametrize("name", sorted(MINDESTGROESSE))
def test_modelldatei_vollstaendig(fc, name):
    datei = fc.MODELLE / name
    assert datei.is_file(), (
        f"{name} fehlt. Nachladen mit:\n  uv run code/tools/modelle_holen.py"
    )
    groesse = datei.stat().st_size
    assert groesse >= MINDESTGROESSE[name], (
        f"{name} ist nur {groesse / 1_000_000:.1f} MB gross und damit "
        f"unvollstaendig (erwartet mindestens "
        f"{MINDESTGROESSE[name] / 1_000_000:.1f} MB). Der Download wurde "
        f"abgebrochen. Neu laden mit:\n"
        f"  uv run code/tools/modelle_holen.py --neu"
    )


def test_yunet_laedt(detektor):
    """YuNet ist der Gesichtsfinder von 2023 (Station 3 und 4)."""
    assert detektor is not None


def test_sface_laedt(erkenner):
    """SFace macht aus einem Gesicht 128 Zahlen (Station 4)."""
    assert erkenner is not None


def test_schwelle_ist_gesetzt(fc):
    """Der Standardschwellenwert steht in faceit und wird in 04c benutzt."""
    assert 0.0 < fc.SCHWELLE < 1.0, (
        f"Der Schwellenwert {fc.SCHWELLE} liegt ausserhalb von 0 bis 1."
    )


def test_landmark_modell_ist_optional(fc):
    """
    lbfmodel.yaml liegt bewusst NICHT im Repository (54 MB). Fehlt es, muss
    Station 3b sauber ausfallen, nicht abstuerzen. Dieser Test meldet nur,
    was da ist - er schlaegt nie fehl.
    """
    datei = fc.MODELLE / "lbfmodel.yaml"
    if not datei.is_file():
        pytest.skip(
            "lbfmodel.yaml fehlt - Station 3b faellt aus, alles andere laeuft. "
            "Nur fuer den Beamer-Rechner noetig:\n"
            "  uv run code/tools/landmark_modell_holen.py"
        )
    assert datei.stat().st_size > 40_000_000, (
        "lbfmodel.yaml ist unvollstaendig. Neu laden mit:\n"
        "  uv run code/tools/landmark_modell_holen.py"
    )
