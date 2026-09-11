"""
Test 6: Der Vergleichssatz in data/personen/

Diese Bilder sind die Beamer-Demo aus Station 4b: mehrere Aufnahmen derselben
Person aus verschiedenen Lebensaltern. Sie werden nur auf dem Beamer-Rechner
gebraucht - auf allen anderen Rechnern ueberspringen diese Tests planmaessig,
genau wie der Test fuer das Landmark-Modell.

Nachladen:
    uv run code/tools/personen_holen.py

Warum hier keine festen Messwerte stehen: Die Bilder liegen nicht im
Repository, sondern werden von Wikimedia Commons geholt. Dort kann eine Datei
jederzeit durch einen besseren Scan ersetzt werden, und schon verschieben sich
alle Aehnlichkeiten. Geprueft werden deshalb nur **Relationen** - die halten
auch dann. Die konkreten Zahlen stehen in data/personen/CREDITS.md und in
docs/03_loesungen.md, mit Messdatum.
"""

import itertools
import subprocess
import sys
from pathlib import Path

import pytest

from test_4_stationen import CODE, PROJEKT, ZEITGRENZE, pruefen, umgebung

PERSONEN = PROJEKT / "data" / "personen"
BEISPIELE = PROJEKT / "data" / "beispiele"

NACHLADEN = ("Nur fuer den Beamer-Rechner noetig:\n"
             "  uv run code/tools/personen_holen.py")


def person(dateiname: str) -> str:
    """'einstein_1920.jpg' -> 'einstein' - die Personenzuordnung steckt im Namen."""
    return dateiname.split("_")[0].replace(".jpg", "")


@pytest.fixture(scope="session")
def dateien():
    gefunden = sorted(PERSONEN.glob("*.jpg"))
    if len(gefunden) < 2:
        pytest.skip(f"data/personen/ hat weniger als zwei Bilder. {NACHLADEN}")
    return gefunden


@pytest.fixture(scope="session")
def vektoren(fc, detektor, erkenner, dateien):
    """
    Die 128 Zahlen je Bild, EINMAL berechnet und dann geteilt.
    Ohne das Caching wuerde jeder Test hier alle Bilder neu durch SFace
    schicken - auf einem Schulrechner dauert das unnoetig lang.
    """
    import cv2

    ergebnis = {}
    for pfad in dateien:
        bild = cv2.imread(str(pfad))
        assert bild is not None, f"Bild laesst sich nicht laden: {pfad}"
        gesichter = fc.gesichter_finden(detektor, bild)
        if len(gesichter) != 1:
            continue
        ergebnis[pfad.name] = fc.gesicht_zu_zahlen(
            erkenner, bild, gesichter[0])
    if len(ergebnis) < 2:
        pytest.skip(f"Weniger als zwei verwertbare Bilder. {NACHLADEN}")
    return ergebnis


@pytest.fixture(scope="session")
def gruppiert(fc, vektoren):
    """Alle Paare, getrennt in 'dieselbe Person' und 'verschiedene Personen'."""
    gleich, fremd = [], []
    for a, b in itertools.combinations(sorted(vektoren), 2):
        wert = fc.aehnlichkeit(vektoren[a], vektoren[b])
        (gleich if person(a) == person(b) else fremd).append((wert, a, b))
    return gleich, fremd


# --------------------------------------------------------------- Struktur

def test_jedes_bild_hat_genau_ein_gesicht(fc, detektor, dateien):
    """
    Bei mehreren oder fehlenden Gesichtern wuesste niemand, wessen Gesicht
    gemessen wird - dann ist das Bild als Vergleichsmaterial unbrauchbar.
    """
    import cv2

    fehler = []
    for pfad in dateien:
        bild = cv2.imread(str(pfad))
        if bild is None:
            fehler.append(f"{pfad.name}: laedt nicht")
            continue
        gesichter = fc.gesichter_finden(detektor, bild)
        if len(gesichter) != 1:
            fehler.append(f"{pfad.name}: {len(gesichter)} Gesichter statt 1")
        elif gesichter[0][2] < 80:
            fehler.append(f"{pfad.name}: Gesicht nur {int(gesichter[0][2])} px breit")
    assert not fehler, "Unbrauchbare Bilder:\n  " + "\n  ".join(fehler)


def test_embeddings_haben_128_zahlen(vektoren):
    for name, zahlen in vektoren.items():
        assert zahlen.size == 128, f"{name} ergibt {zahlen.size} Zahlen statt 128"


def test_jedes_bild_ist_sich_selbst_aehnlich(fc, vektoren):
    for name, zahlen in vektoren.items():
        wert = fc.aehnlichkeit(zahlen, zahlen)
        assert wert > 0.99, f"{name} mit sich selbst ergibt nur {wert:.3f}"


def test_aehnlichkeit_ist_symmetrisch(fc, vektoren):
    namen = sorted(vektoren)[:2]
    hin = fc.aehnlichkeit(vektoren[namen[0]], vektoren[namen[1]])
    her = fc.aehnlichkeit(vektoren[namen[1]], vektoren[namen[0]])
    assert hin == pytest.approx(her, abs=1e-6)


# ------------------------------------------------------------ Der Bestand

def test_mindestens_zwei_personen(vektoren):
    schluessel = {person(n) for n in vektoren}
    assert len(schluessel) >= 2, (
        f"Nur die Person '{list(schluessel)[0]}' ist vorhanden - "
        f"dann gibt es keine Fremdvergleiche. {NACHLADEN}"
    )


def test_mindestens_eine_person_mehrfach(vektoren):
    """Das ist der ganze Sinn dieses Ordners: dieselbe Person zweimal."""
    zaehler = {}
    for name in vektoren:
        zaehler[person(name)] = zaehler.get(person(name), 0) + 1
    mehrfach = {p: n for p, n in zaehler.items() if n >= 2}
    assert mehrfach, (
        "Keine Person ist mehrfach vertreten. Genau dafuer gibt es diesen "
        f"Ordner - sonst reicht data/beispiele/. {NACHLADEN}"
    )


# --------------------------------------------------- Relationen (robust)

def test_gleiche_person_ist_im_schnitt_aehnlicher(gruppiert):
    """
    Die Grundaussage von Station 4: Aufnahmen derselben Person liegen naeher
    zusammen. Geprueft als Mittelwert ueber alle Paare, nicht an einem
    einzelnen Paar - deshalb stabil gegen ein ausgetauschtes Bild.
    """
    gleich, fremd = gruppiert
    if not gleich or not fremd:
        pytest.skip("Es fehlen Paare fuer den Vergleich")
    schnitt_gleich = sum(w for w, _, _ in gleich) / len(gleich)
    schnitt_fremd = sum(w for w, _, _ in fremd) / len(fremd)
    assert schnitt_gleich > schnitt_fremd, (
        f"Dieselbe Person im Schnitt {schnitt_gleich:.3f}, verschiedene "
        f"Personen {schnitt_fremd:.3f}. Die Erkennung arbeitet nicht richtig - "
        "oder eine Datei zeigt eine andere Person als ihr Name sagt."
    )


def test_bestes_gleich_paar_schlaegt_bestes_fremd_paar(gruppiert):
    """Wenn das nicht mehr gilt, ist das Modell kaputt - nicht die Auswahl."""
    gleich, fremd = gruppiert
    if not gleich or not fremd:
        pytest.skip("Es fehlen Paare fuer den Vergleich")
    hoechstes_gleich = max(gleich)
    hoechstes_fremd = max(fremd)
    assert hoechstes_gleich[0] > hoechstes_fremd[0], (
        f"Bestes Gleich-Paar {hoechstes_gleich[0]:.3f} "
        f"({hoechstes_gleich[1]} <-> {hoechstes_gleich[2]}) liegt nicht ueber "
        f"dem besten Fremd-Paar {hoechstes_fremd[0]:.3f} "
        f"({hoechstes_fremd[1]} <-> {hoechstes_fremd[2]})."
    )


def test_mindestens_ein_gleich_paar_wird_erkannt(fc, gruppiert):
    gleich, _ = gruppiert
    if not gleich:
        pytest.skip("Keine Aufnahmen derselben Person vorhanden")
    bestes = max(gleich)
    assert bestes[0] >= fc.SCHWELLE, (
        f"Kein einziges Paar derselben Person erreicht die Schwelle "
        f"{fc.SCHWELLE:.3f}. Bestes: {bestes[0]:.3f} "
        f"({bestes[1]} <-> {bestes[2]})."
    )


def test_ueberlappung_ist_noch_messbar(fc, gruppiert):
    """
    Die didaktische Pointe: das schlechteste Gleich-Paar liegt UNTER dem besten
    Fremd-Paar. Das ist eine Eigenschaft der Bilder, nicht des Codes - und die
    Bilder liegen nicht im Repository. Faellt die Ueberlappung weg, ist das
    kein Defekt, sondern ein Hinweis, dass die Tabelle in docs/03_loesungen.md
    neu gemessen werden muss. Deshalb hier ein skip und kein Fehler.
    """
    gleich, fremd = gruppiert
    if not gleich or not fremd:
        pytest.skip("Es fehlen Paare fuer den Vergleich")
    tiefstes_gleich = min(gleich)
    hoechstes_fremd = max(fremd)
    if tiefstes_gleich[0] >= hoechstes_fremd[0]:
        pytest.skip(
            f"Keine Ueberlappung mehr messbar (schlechtestes Gleich-Paar "
            f"{tiefstes_gleich[0]:.3f} >= bestes Fremd-Paar "
            f"{hoechstes_fremd[0]:.3f}). Wahrscheinlich hat Commons ein Bild "
            f"ersetzt. Neu messen mit "
            f"'uv run code/tools/personen_holen.py --messen' und die Tabelle "
            f"in docs/03_loesungen.md nachziehen."
        )
    assert tiefstes_gleich[0] < hoechstes_fremd[0]


# ----------------------------------------------- Die beiden Ordner trennen

def test_kein_beispielportrait_in_personen(dateien):
    """
    data/beispiele/ und data/personen/ haben verschiedene Zwecke und
    verschiedene Lizenzlagen. Sie duerfen sich nicht vermischen.
    """
    falsch = [p.name for p in dateien if p.name.startswith("portrait_")]
    assert not falsch, (
        f"Diese Dateien gehoeren nach data/beispiele/: {falsch}"
    )


def test_keine_doppelte_person_in_beispielen(fc, detektor, erkenner):
    """
    Gegenprobe zur Trennung: In data/beispiele/ darf keine Person zweimal
    vorkommen - tests/test_3_erkennung.py verlaesst sich darauf. Mehrfach-
    aufnahmen gehoeren nach data/personen/.
    """
    import cv2

    bilder = sorted(BEISPIELE.glob("portrait_*.jpg"))
    if len(bilder) < 2:
        pytest.skip("Zu wenige Beispielportraits fuer die Gegenprobe")

    zahlen = {}
    for pfad in bilder:
        bild = cv2.imread(str(pfad))
        gesichter = fc.gesichter_finden(detektor, bild)
        if len(gesichter) == 1:
            zahlen[pfad.name] = fc.gesicht_zu_zahlen(erkenner, bild, gesichter[0])

    for a, b in itertools.combinations(sorted(zahlen), 2):
        wert = fc.aehnlichkeit(zahlen[a], zahlen[b])
        assert wert < fc.SCHWELLE, (
            f"{a} und {b} erreichen {wert:.3f} - das sieht nach derselben "
            "Person aus. Mehrfachaufnahmen gehoeren nach data/personen/, "
            "sonst schlaegt test_3_erkennung.py fehl."
        )


# --------------------------------------- Station 4b im Dateimodus starten

def test_04b_vergleicht_zwei_dateien(dateien, tmp_path):
    """
    Der Code-Pfad, auf dem dieser ganze Bildsatz aufsetzt:
    04b_vergleich.py mit ZWEI DATEIPFADEN statt mit der Kamera
    (code/04b_vergleich.py Zeile 55-57).

    tests/test_4_stationen.py startet 04b nur im Live-Zweig mit Tastendruecken -
    dieser Zweig war bis hierher von keinem Test beruehrt.

    Geprueft wird nur die Struktur, kein Zahlenwert.
    """
    lauf = subprocess.run(
        [sys.executable, str(CODE / "04b_vergleich.py"),
         str(dateien[0]), str(dateien[1])],
        env=umgebung(tmp_path), input="", capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=ZEITGRENZE, cwd=str(PROJEKT),
    )
    pruefen(lauf, "04b_vergleich.py (Dateimodus)")
    assert "Aehnlichkeit" in lauf.stdout, (
        f"04b hat keinen Aehnlichkeitswert ausgegeben:\n{lauf.stdout[-800:]}"
    )
    assert "Schwelle" in lauf.stdout


def test_04b_meldet_fehlende_datei_verstaendlich(tmp_path):
    """
    Wenn die Lehrkraft sich am Beamer vertippt, muss eine lesbare Meldung
    kommen und kein Traceback.
    """
    lauf = subprocess.run(
        [sys.executable, str(CODE / "04b_vergleich.py"),
         "data/personen/gibtsnicht.jpg", "data/personen/auchnicht.jpg"],
        env=umgebung(tmp_path), input="", capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=ZEITGRENZE, cwd=str(PROJEKT),
    )
    ausgabe = (lauf.stdout or "") + (lauf.stderr or "")
    assert "Traceback" not in ausgabe, (
        f"04b bricht mit einer Ausnahme ab statt mit einer Meldung:\n"
        f"{ausgabe[-800:]}"
    )
    assert "laesst sich nicht laden" in ausgabe or "nicht laden" in ausgabe, (
        f"Keine verstaendliche Fehlermeldung:\n{ausgabe[-800:]}"
    )


def test_99_cleanup_schont_die_vergleichsgesichter(dateien):
    """
    Wie data/beispiele/ sind das keine Daten von SuS, sondern freie Bilder
    aus dem Netz. Sie muessen das Loeschritual am Ende jedes Termins
    ueberleben - sonst fehlen sie beim naechsten Mal.

    Die Positivliste ZU_LOESCHEN in code/99_cleanup.py (Zeile 23-29) nennt
    'personen' nicht, der Ordner bleibt also. Dieser Test haelt das fest,
    damit es beim naechsten Umbau nicht verloren geht.
    """
    cleanup = PROJEKT / "code" / "99_cleanup.py"
    quelltext = cleanup.read_text(encoding="utf-8")
    # Grob, aber ausreichend: kommt 'personen' in der Loeschliste vor?
    beginn = quelltext.find("ZU_LOESCHEN")
    ende = quelltext.find("]", beginn)
    liste = quelltext[beginn:ende]
    assert "personen" not in liste, (
        "code/99_cleanup.py loescht jetzt data/personen/. Die Vergleichs"
        "gesichter sind freie Bilder aus dem Netz und keine Daten von SuS - "
        "sie sollen bleiben, wie data/beispiele/ auch."
    )
    assert "beispiele" not in liste, (
        "code/99_cleanup.py loescht jetzt data/beispiele/. Das sind die "
        "Ersatzgesichter fuer SuS, die sich nicht fotografieren lassen."
    )
    assert dateien, "Die Vergleichsgesichter sind verschwunden."
