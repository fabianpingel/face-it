"""
Station 4b - Wie aehnlich sind zwei Gesichter?

Du nimmst zwei Gesichter auf und das Programm vergleicht ihre 128 Zahlen.
Das Ergebnis ist eine einzige Zahl zwischen -1 und +1:

    1.00  die Zahlenlisten zeigen in genau dieselbe Richtung
    0.00  sie haben nichts miteinander zu tun

Ab welchem Wert gilt "dieselbe Person"? Das hat jemand festgelegt.
Bei diesem Modell liegt die Grenze bei 0.363. Warum genau da?
Weil man irgendwo eine Grenze ziehen muss.

Testreihe fuer dein Handout:
    ich  -  ich                     (gleiches Licht)
    ich  -  ich                     (Brille ab, Haare anders, Grimasse)
    ich  -  Nachbarin oder Nachbar
    ich  -  Portrait aus data/beispiele

Starten:
    uv run code/05_vergleich.py
    uv run code/05_vergleich.py bild1.jpg bild2.jpg    (zwei Dateien vergleichen)
"""

import sys

import cv2
import numpy as np

import faceit


def aus_datei(pfad, detektor, erkenner):
    bild = cv2.imread(str(pfad))
    if bild is None:
        faceit.abbruch(f"Diese Datei laesst sich nicht laden: {pfad}")
    gesichter = faceit.gesichter_finden(detektor, bild)
    if not gesichter:
        faceit.abbruch(f"In diesem Bild ist kein Gesicht zu finden: {pfad}")
    gesicht = max(gesichter, key=lambda g: g[2] * g[3])
    return (faceit.gesicht_zu_zahlen(erkenner, bild, gesicht),
            erkenner.alignCrop(bild, gesicht))


def urteil(wert):
    if wert >= faceit.SCHWELLE:
        return "DIESELBE PERSON", faceit.GRUEN
    return "VERSCHIEDENE PERSONEN", faceit.ROT


detektor = faceit.detektor_laden()
erkenner = faceit.erkenner_laden()

# --------------------------------------------------- Variante 1: zwei Dateien
if len(sys.argv) > 2:
    vektor_a, bild_a = aus_datei(sys.argv[1], detektor, erkenner)
    vektor_b, bild_b = aus_datei(sys.argv[2], detektor, erkenner)
    wert = faceit.aehnlichkeit(vektor_a, vektor_b)
    text, farbe = urteil(wert)
    faceit.titel("Station 4b - Vergleich zweier Bilder",
                 f"{sys.argv[1]}", f"{sys.argv[2]}")
    print(f"  Aehnlichkeit: {wert:+.3f}   ({wert * 100:.0f} Prozent)")
    print(f"  Schwelle:     {faceit.SCHWELLE:+.3f}")
    print(f"  Urteil:       {text}")
    print()
    zusammen = np.hstack([cv2.resize(bild_a, (300, 300)),
                          cv2.resize(bild_b, (300, 300))])
    faceit.schrift(zusammen, text, (16, 40), farbe, 0.8, 2)
    faceit.zeigen("Face it - Vergleich", zusammen)
    if not faceit.TESTMODUS:
        cv2.waitKey(0)
    faceit.fenster_schliessen()
    sys.exit(0)

# --------------------------------------------------- Variante 2: live
faceit.titel(
    "Station 4b - Wie aehnlich sind zwei Gesichter?",
    "[1] linkes Gesicht aufnehmen",
    "[2] rechtes Gesicht aufnehmen",
    "[r] zuruecksetzen        [q] beenden",
)

kamera = faceit.kamera_oeffnen()
gespeichert = {}
leer = np.full((300, 300, 3), 35, np.uint8)

while True:
    bild = faceit.bild_holen(kamera)
    gesichter = faceit.gesichter_finden(detektor, bild)
    for gesicht in gesichter:
        faceit.gesichtsrahmen(bild, gesicht, faceit.CYAN)

    links = gespeichert.get("1", (None, leer))[1]
    rechts = gespeichert.get("2", (None, leer))[1]
    kachel_a = cv2.resize(links, (300, 300))
    kachel_b = cv2.resize(rechts, (300, 300))
    faceit.schrift(kachel_a, "1", (12, 40), faceit.CYAN, 1.0, 2)
    faceit.schrift(kachel_b, "2", (12, 40), faceit.CYAN, 1.0, 2)

    tafel = np.full((300, 420, 3), 25, np.uint8)
    if "1" in gespeichert and "2" in gespeichert:
        wert = faceit.aehnlichkeit(gespeichert["1"][0], gespeichert["2"][0])
        text, farbe = urteil(wert)
        faceit.schrift(tafel, "Aehnlichkeit", (20, 46), faceit.GRAU, 0.7, 1)
        faceit.schrift(tafel, f"{wert * 100:.0f} %", (20, 120), farbe, 2.0, 4)
        faceit.balken(tafel, max(0.0, wert), (20, 150), 380, 26, farbe)
        # Wo liegt die Schwelle auf dem Balken?
        x_schwelle = 20 + int(380 * faceit.SCHWELLE)
        cv2.line(tafel, (x_schwelle, 144), (x_schwelle, 182), faceit.WEISS, 2)
        faceit.schrift(tafel, f"Schwelle {faceit.SCHWELLE:.3f}",
                       (20, 208), faceit.WEISS, 0.5, 1)
        faceit.schrift(tafel, text, (20, 250), farbe, 0.7, 2)
    else:
        faceit.schrift(tafel, "Nimm zwei Gesichter auf:", (20, 120),
                       faceit.WEISS, 0.65, 1)
        faceit.schrift(tafel, "[1] links      [2] rechts", (20, 158),
                       faceit.CYAN, 0.65, 1)

    kamerabild = cv2.resize(bild, (420, 300))
    zusammen = np.hstack([kachel_a, kachel_b, tafel, kamerabild])
    faceit.hinweisleiste(zusammen, ["[1] links   [2] rechts   [r] neu   [q] beenden"])
    faceit.zeigen("Face it - Station 4b", zusammen)

    gedrueckt = faceit.taste()

    if gedrueckt in ("1", "2"):
        if not gesichter:
            print("  Kein Gesicht im Bild.")
            continue
        gesicht = max(gesichter, key=lambda g: g[2] * g[3])
        gespeichert[gedrueckt] = (
            faceit.gesicht_zu_zahlen(erkenner, bild, gesicht),
            erkenner.alignCrop(bild, gesicht),
        )
        seite = "links" if gedrueckt == "1" else "rechts"
        print(f"  Gesicht {seite} aufgenommen.")
        if len(gespeichert) == 2:
            wert = faceit.aehnlichkeit(gespeichert["1"][0], gespeichert["2"][0])
            text, _ = urteil(wert)
            print(f"  Aehnlichkeit: {wert:+.3f}  ->  {text}")

    elif gedrueckt == "r":
        gespeichert.clear()
        print("  Zurueckgesetzt.")

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 4c: uv run code/06_faceid.py")
print()
