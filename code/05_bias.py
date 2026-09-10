"""
Station 5 - Fehler, Schwellenwerte und Bias.

Dieses Programm braucht keine Kamera. Es rechnet mit den Gesichtern,
die deine Klasse in Station 4 aufgenommen hat.

Teil 1 rechnet mit euren echten Daten:
    Wie aehnlich sind zwei Bilder derselben Person?
    Wie aehnlich sind zwei Bilder verschiedener Personen?
    Ueberlappen sich diese beiden Bereiche? (Spoiler: ja.)
    Welche Schwelle macht die wenigsten Fehler?

Teil 2 zeigt Zahlen aus veroeffentlichten Studien:
    Dieselbe Technik macht bei verschiedenen Menschengruppen
    unterschiedlich viele Fehler. Das ist gemessen, nicht behauptet.

Starten:
    uv run code/05_bias.py
"""

import sys
from itertools import combinations

import numpy as np

import faceit


def person_aus_dateiname(pfad):
    """Aus 'mia_02.npy' wird 'mia'."""
    name = pfad.stem
    return name.rsplit("_", 1)[0] if "_" in name else name


def histogramm(werte, beschriftung, breite=44):
    """Zeichnet eine einfache Verteilung aus Textzeichen."""
    if not werte:
        return
    print(f"  {beschriftung}  (n = {len(werte)})")
    stufen = np.arange(-0.2, 1.05, 0.1)
    for untere in stufen[:-1]:
        obere = untere + 0.1
        anzahl = sum(1 for w in werte if untere <= w < obere)
        balken = "#" * int(round(breite * anzahl / len(werte)))
        print(f"    {untere:+.1f} bis {obere:+.1f} | {balken:<{breite}} {anzahl}")
    print()


def fehlertabelle(gleiche, verschiedene):
    """
    Zeigt fuer verschiedene Schwellen, wie viele Fehler entstehen.
      Falsch abgewiesen: dieselbe Person wird nicht erkannt.
      Falsch akzeptiert: eine fremde Person wird durchgelassen.
    """
    print("  Was passiert bei welcher Schwelle?")
    print()
    print("   Schwelle | falsch abgewiesen | falsch akzeptiert | Fehler gesamt")
    print("   ---------+-------------------+-------------------+--------------")
    beste = None
    for schwelle in [i / 20 for i in range(1, 17)]:
        abgewiesen = sum(1 for w in gleiche if w < schwelle)
        akzeptiert = sum(1 for w in verschiedene if w >= schwelle)
        gesamt = abgewiesen + akzeptiert
        marke = ""
        if schwelle - 0.025 < faceit.SCHWELLE <= schwelle + 0.025:
            marke = "  <- Standard des Modells"
        print(f"     {schwelle:5.2f}  |  {abgewiesen:3d} von {len(gleiche):3d}"
              f"      |  {akzeptiert:3d} von {len(verschiedene):3d}"
              f"      |  {gesamt:3d}{marke}")
        if beste is None or gesamt < beste[1]:
            beste = (schwelle, gesamt)
    print()
    if beste:
        print(f"  Am wenigsten Fehler bei Schwelle {beste[0]:.2f}: "
              f"{beste[1]} Fehler insgesamt.")
    print()


def teil1():
    ordner = faceit.daten_ordner("gesichter")
    dateien = sorted(ordner.glob("*.npy"))

    faceit.titel("Teil 1 - Eure eigenen Daten",
                 f"{len(dateien)} Aufnahmen in {ordner}")

    if len(dateien) < 4:
        print("  Dafuer sind noch zu wenige Gesichter gespeichert.")
        print("  Geht zurueck zu Station 4a und nehmt pro Person")
        print("  mindestens zwei Fotos auf:")
        print()
        print("      uv run code/04a_embedding.py Vorname")
        print()
        return False

    vektoren = {pfad: np.load(pfad) for pfad in dateien}
    personen = {pfad: person_aus_dateiname(pfad) for pfad in dateien}
    print(f"  Personen: {', '.join(sorted(set(personen.values())))}")
    print()

    gleiche, verschiedene = [], []
    for a, b in combinations(dateien, 2):
        wert = faceit.aehnlichkeit(vektoren[a], vektoren[b])
        (gleiche if personen[a] == personen[b] else verschiedene).append(wert)

    if not gleiche:
        print("  Es gibt noch kein Paar von zwei Bildern DERSELBEN Person.")
        print("  Nehmt von einer Person ein zweites Foto auf - dann wird")
        print("  der Vergleich interessant.")
        print()
    else:
        histogramm(gleiche, "Zwei Bilder DERSELBEN Person")
    histogramm(verschiedene, "Zwei Bilder VERSCHIEDENER Personen")

    if gleiche and verschiedene:
        print(f"  Dieselbe Person:        von {min(gleiche):+.2f} "
              f"bis {max(gleiche):+.2f}")
        print(f"  Verschiedene Personen:  von {min(verschiedene):+.2f} "
              f"bis {max(verschiedene):+.2f}")
        if min(gleiche) < max(verschiedene):
            print()
            print("  Die beiden Bereiche UEBERLAPPEN sich.")
            print("  Das heisst: Es gibt keine Schwelle, die alles richtig macht.")
            print("  Jede Schwelle ist ein Kompromiss zwischen zwei Fehlerarten.")
        else:
            print()
            print("  Bei euch trennen sich die Bereiche noch sauber.")
            print("  Nehmt schwierigere Bilder auf: schlechtes Licht, Brille,")
            print("  Kopf zur Seite, Grimasse. Dann verschwindet die Luecke.")
        print()
        fehlertabelle(gleiche, verschiedene)
    return True


def teil2():
    faceit.titel("Teil 2 - Was Studien gemessen haben",
                 "Diese Zahlen sind veroeffentlicht und nachpruefbar.")

    print("  Gender Shades, Buolamwini und Gebru, MIT, 2018")
    print("  Untersucht wurden drei kommerzielle Systeme, die aus einem Foto")
    print("  das Geschlecht bestimmen sollten.")
    print()
    print("    Gruppe                        Fehlerrate")
    print("    ----------------------------  ----------")
    for gruppe, rate in [("hellhaeutige Maenner", 0.8),
                         ("hellhaeutige Frauen", 7.1),
                         ("dunkelhaeutige Maenner", 12.0),
                         ("dunkelhaeutige Frauen", 34.7)]:
        balken = "#" * int(round(rate))
        print(f"    {gruppe:<28}  {rate:5.1f} %  {balken}")
    print()
    print("  Ein System, das bei einer Gruppe fast nie irrt und bei einer")
    print("  anderen bei jedem dritten Bild - und beides ist dasselbe Programm.")
    print()
    print("  NIST FRVT Part 3, 2019 (US-Bundesbehoerde, 189 Algorithmen)")
    print("  Beim Vergleich zweier Gesichter lag die Rate der falschen")
    print("  Treffer bei west- und ostafrikanischen sowie ostasiatischen")
    print("  Gesichtern bei vielen Algorithmen 10- bis 100-mal hoeher")
    print("  als bei osteuropaeischen Gesichtern.")
    print()
    print("  Was das praktisch bedeutet:")
    print()
    print("    Schwelle so gewaehlt, dass Gruppe A einen Fehltreffer")
    print("    auf 10.000 Vergleiche hat. Dann bekommt")
    print("      Gruppe B (Faktor 10):   1 Fehltreffer auf  1.000")
    print("      Gruppe C (Faktor 100):  1 Fehltreffer auf    100")
    print()
    print("  Bei einer Fahndung mit 100.000 Kameraaufnahmen pro Tag sind das")
    print("  10 gegenueber 1.000 Menschen, die faelschlich verdaechtigt werden.")
    print()
    print("  Woran liegt das? An den Trainingsdaten. Ein Modell lernt aus")
    print("  Millionen Fotos - und wer darauf selten vorkommt, wird schlechter")
    print("  erkannt. Das Modell ist nicht boshaft. Es ist einseitig gefuettert.")
    print()


def schluss():
    print("  " + "=" * 62)
    print("  Drei Fragen, die ihr jetzt beantworten koennt:")
    print("  " + "=" * 62)
    print("  1. Wer legt die Schwelle fest - und wer traegt die Folgen?")
    print("  2. Ein Passwort kann man aendern. Was macht man mit einem")
    print("     Gesicht, das einmal in einer Datenbank gelandet ist?")
    print("  3. Wuerdet ihr diese Technik am Bahnhof einsetzen? Und wenn ja:")
    print("     Welche Fehlerrate waere euch bei euch selbst noch recht?")
    print()


if len(sys.argv) > 1 and sys.argv[1] == "--nur-studien":
    teil2()
    schluss()
else:
    teil1()
    teil2()
    schluss()
