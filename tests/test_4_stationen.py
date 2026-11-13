"""
Test 4: Startet jede Station ohne Absturz?

Jedes Stationsskript wird als eigener Prozess gestartet - genau so, wie es
eine Gruppe im Workshop tun wuerde, nur ohne Bildschirm und ohne Webcam:

  FACEIT_KAMERA   ersetzt die Webcam durch ein Portrait
  FACEIT_TASTEN   speist Tastendruecke ein; ist die Folge zu Ende, kommt "q"
  FACEIT_DATEN    lenkt alle Schreibvorgaenge in data/_testlauf/

Dieser Test findet genau die Fehler, die sonst erst auffallen, wenn 20 SuS
davor sitzen: Tippfehler in einer selten benutzten Zeile, ein fehlendes
Modell, eine kaputte Ausgabe.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJEKT = Path(__file__).resolve().parent.parent
CODE = PROJEKT / "code"
PORTRAIT = PROJEKT / "data" / "beispiele" / "portrait_01.jpg"

# Zeit, die ein Skript hoechstens brauchen darf. SFace ist 37 MB, das Laden
# dauert auf langsamen Schulrechnern ein paar Sekunden.
ZEITGRENZE = 120

# Die Stationen in der Reihenfolge des Workshops.
# (Skript, Tastenfolge, Eingabe auf die Frage nach dem Namen)
STATIONEN = [
    ("00_check.py", "q", None),
    ("01_pixel.py", "z q", None),
    ("02_filter.py", "123456q", None),
    ("03_detect.py", "yyq", None),
    ("04b_vergleich.py", "12q", None),
    ("04c_faceid.py", " q", None),
]

# Advanced-Programme. Sie brauchen die Aufnahmen aus 04a, deshalb laufen sie
# erst, nachdem die Testdaten angelegt sind.
ADVANCED = [
    ("94_kernel_labor.py", "q", None),
    ("93_durchschnitt.py", "q", None),
    ("91_gesichtsraum.py", "q", None),
    ("92_fehlerkurve.py", "q", None),
    ("90_anwesenheit.py", "q", None),
]


def umgebung(datenordner: Path, tasten: str = "q") -> dict:
    """Baut die Umgebungsvariablen fuer einen Stationsstart."""
    umg = dict(os.environ)
    umg["FACEIT_TEST"] = "1"
    umg["FACEIT_KAMERA"] = str(PORTRAIT)
    umg["FACEIT_TASTEN"] = tasten
    umg["FACEIT_DATEN"] = str(datenordner)
    umg["PYTHONIOENCODING"] = "utf-8"
    return umg


def starten(skript: str, datenordner: Path, tasten: str = "q", eingabe=None):
    """Startet ein Stationsskript und gibt das Ergebnis zurueck."""
    return subprocess.run(
        [sys.executable, str(CODE / skript)],
        env=umgebung(datenordner, tasten),
        input=eingabe if eingabe is not None else "",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=ZEITGRENZE,
        cwd=str(PROJEKT),
    )


def pruefen(lauf, skript):
    """Gemeinsame Auswertung: Exit-Code 0 und keine Ausnahme in der Ausgabe."""
    ausgabe = (lauf.stdout or "") + (lauf.stderr or "")
    assert "Traceback" not in ausgabe, (
        f"{skript} ist mit einer Ausnahme abgebrochen:\n{ausgabe[-1500:]}"
    )
    assert lauf.returncode == 0, (
        f"{skript} endete mit Exit-Code {lauf.returncode}:\n{ausgabe[-1500:]}"
    )


@pytest.fixture(scope="module")
def klassendaten(fc, portraits, tmp_path_factory):
    """
    Simuliert, was eine Klasse in Station 4a aufnimmt: zwei Personen mit je
    zwei Aufnahmen. Das ergibt vier Vektoren mit zwei Paaren - das Minimum,
    das 05_bias.py fuer seine beiden Verteilungen braucht.
    """
    ordner = tmp_path_factory.mktemp("klassendaten")

    for name in ("anna", "ben"):
        lauf = starten("04a_embedding.py", ordner, tasten="  q", eingabe=f"{name}\n")
        pruefen(lauf, f"04a_embedding.py ({name})")

    vektoren = sorted((ordner / "gesichter").glob("*.npy"))
    assert len(vektoren) == 4, (
        f"Erwartet wurden 4 Vektoren, angelegt wurden {len(vektoren)}: "
        f"{[v.name for v in vektoren]}"
    )
    return ordner


# ------------------------------------------------------- die einzelnen Stationen

def test_04a_legt_vektoren_an(klassendaten):
    """Station 4a ist die einzige Station, die dauerhaft speichert."""
    vektoren = sorted((klassendaten / "gesichter").glob("*.npy"))
    namen = {v.name.split("_")[0] for v in vektoren}
    assert namen == {"anna", "ben"}
    for v in vektoren:
        assert v.stat().st_size > 0, f"{v.name} ist leer."


@pytest.mark.parametrize("skript,tasten,eingabe", STATIONEN,
                         ids=[s[0] for s in STATIONEN])
def test_station_startet(klassendaten, skript, tasten, eingabe):
    pruefen(starten(skript, klassendaten, tasten, eingabe), skript)


def test_03b_landmarks(fc, klassendaten):
    """Station 3b ist Kuer - ohne lbfmodel.yaml wird sie uebersprungen."""
    if not (fc.MODELLE / "lbfmodel.yaml").is_file():
        pytest.skip(
            "lbfmodel.yaml fehlt (nur fuer den Beamer-Rechner noetig): "
            "uv run code/tools/landmark_modell_holen.py"
        )
    pruefen(starten("03b_landmarks.py", klassendaten, "nnq"), "03b_landmarks.py")


def test_05_bias_nur_studien(klassendaten):
    """Der Notfallweg aus der Agenda: nur die veroeffentlichten Zahlen."""
    lauf = subprocess.run(
        [sys.executable, str(CODE / "05_bias.py"), "--nur-studien"],
        env=umgebung(klassendaten), input="", capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=ZEITGRENZE, cwd=str(PROJEKT),
    )
    pruefen(lauf, "05_bias.py --nur-studien")
    assert "Gender Shades" in lauf.stdout


def test_05_bias_rechnet_mit_klassendaten(klassendaten):
    """
    Mit vier Aufnahmen und zwei Paaren muss die Messung durchlaufen und beide
    Verteilungen zeigen - das ist die Grundlage von Block 6.
    """
    lauf = starten("05_bias.py", klassendaten)
    pruefen(lauf, "05_bias.py")
    assert "zu wenige" not in lauf.stdout, (
        "05_bias.py hat die Messung uebersprungen, obwohl vier Aufnahmen da "
        f"sind:\n{lauf.stdout[-1200:]}"
    )


@pytest.mark.parametrize("skript,tasten,eingabe", ADVANCED,
                         ids=[s[0] for s in ADVANCED])
def test_advanced_startet(klassendaten, skript, tasten, eingabe):
    """Die Advanced-Programme sind auch das Take-home-Material."""
    pruefen(starten(skript, klassendaten, tasten, eingabe), skript)


def test_99_cleanup_loescht_wirklich(portraits, tmp_path):
    """
    Das Schlussritual. Laeuft in einem eigenen Ordner, damit dieser Test
    nichts anfassen kann, was ein anderer Test noch braucht.
    """
    eigener = tmp_path / "zumloeschen"
    lauf = starten("04a_embedding.py", eigener, tasten="  q", eingabe="wegdamit\n")
    pruefen(lauf, "04a_embedding.py (fuer den Loeschtest)")

    vorher = list((eigener / "gesichter").glob("*.npy"))
    assert vorher, "Vor dem Loeschtest wurden keine Vektoren angelegt."

    lauf = starten("99_cleanup.py", eigener)
    pruefen(lauf, "99_cleanup.py")

    nachher = list((eigener / "gesichter").glob("*.npy"))
    assert not nachher, (
        f"99_cleanup.py hat {len(nachher)} Vektoren stehen gelassen. "
        "Am Ende jedes Termins muss der Ordner leer sein."
    )


def test_99_cleanup_schont_die_beispielportraits(portraits):
    """
    Die freien Portraits in data/beispiele/ sind keine Daten von SuS und
    muessen das Loeschen ueberleben - sonst fehlen sie beim naechsten Termin.
    """
    assert PORTRAIT.is_file(), (
        "portrait_01.jpg fehlt. Nachladen mit: "
        "uv run code/tools/portraits_holen.py"
    )
