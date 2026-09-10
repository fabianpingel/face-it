"""
Advanced - Das Durchschnittsgesicht.

Das Modell schneidet jedes Gesicht auf genau 112 x 112 Pixel zurecht und
dreht es dabei gerade - Augen immer an derselben Stelle. Genau deshalb
kann man Gesichter miteinander verrechnen wie Zahlen.

Dieses Programm macht zwei Dinge:

    1. Es bildet den Mittelwert aller Gesichter aus Station 4a.
       Das Ergebnis ist ein Gesicht, das niemandem gehoert.
    2. Mit dem Schieberegler blendest du zwischen zwei Gesichtern hin
       und her. Bei 50 Prozent siehst du deren Mittelwert.

Mathematisch ist das nichts anderes als
    Ergebnis = (1 - t) * Bild A  +  t * Bild B
also dieselbe Rechnung, die ihr aus dem Unterricht als Verbindungsstrecke
zwischen zwei Punkten kennt - nur mit 37 632 Zahlen gleichzeitig.

Tasten:
    Schieberegler   Mischung zwischen den beiden Gesichtern
    n               naechstes Gesichterpaar
    q               beenden

Starten:
    uv run code/93_durchschnitt.py
"""

import cv2
import numpy as np

import faceit

FENSTER = "Face it - Durchschnittsgesicht"
REGLER = "Mischung in Prozent"


def gesichter_laden():
    """Laedt die zugeschnittenen Gesichtsbilder aus Station 4a."""
    ordner = faceit.daten_ordner("gesichter")
    dateien = sorted(ordner.glob("*.png"))
    if len(dateien) < 2:
        faceit.abbruch(
            f"Es sind nur {len(dateien)} Gesichtsbilder gespeichert.",
            "Nimm in Station 4a mindestens zwei Aufnahmen auf:",
            "   uv run code/04a_embedding.py Vorname",
        )
    bilder, namen = [], []
    for pfad in dateien:
        bild = cv2.imread(str(pfad))
        if bild is not None:
            bilder.append(cv2.resize(bild, (112, 112)))
            namen.append(pfad.stem)
    return bilder, namen


def gross(bild, kante=336):
    return cv2.resize(bild, (kante, kante), interpolation=cv2.INTER_LINEAR)


bilder, namen = gesichter_laden()

# Der Mittelwert aller Gesichter. In float rechnen, sonst laeuft uint8 ueber.
mittelwert = np.mean([b.astype(np.float32) for b in bilder],
                     axis=0).astype(np.uint8)

faceit.titel(
    "Advanced - Das Durchschnittsgesicht",
    f"{len(bilder)} Gesichter aus Station 4a",
    "[Schieberegler] mischen    [n] naechstes Paar    [q] beenden",
)
print(f"  Der Mittelwert aus {len(bilder)} Gesichtern ist ein Gesicht,")
print("  das keiner einzigen Person gehoert.")
print()

ziel = faceit.daten_ordner("fotos") / "durchschnittsgesicht.png"
cv2.imwrite(str(ziel), gross(mittelwert, 448))
print(f"  Gespeichert: {ziel}")
print()

faceit.fenster(FENSTER)
faceit.regler_anlegen(FENSTER, REGLER, 50, 100)

paar = 0

while True:
    a = bilder[paar % len(bilder)]
    b = bilder[(paar + 1) % len(bilder)]
    name_a = namen[paar % len(namen)]
    name_b = namen[(paar + 1) % len(namen)]

    t = faceit.regler_wert(FENSTER, REGLER) / 100
    mischung = cv2.addWeighted(a, 1 - t, b, t, 0)

    kacheln = [gross(a), gross(mischung), gross(b), gross(mittelwert)]
    beschriftung = [name_a, f"{(1 - t) * 100:.0f}% + {t * 100:.0f}%",
                    name_b, f"Mittel aus {len(bilder)}"]
    for kachel, text in zip(kacheln, beschriftung):
        faceit.schrift(kachel, text, (12, 30), faceit.CYAN, 0.6, 2)

    zusammen = np.hstack(kacheln)
    faceit.hinweisleiste(zusammen, [
        "[Schieberegler] mischen   [n] naechstes Paar   [q] beenden"])
    faceit.zeigen(FENSTER, zusammen)
    faceit.fenster_anpassen(FENSTER, zusammen)

    gedrueckt = faceit.taste()
    if gedrueckt == "q":
        break
    if gedrueckt == "n":
        paar += 1
        print(f"  Paar: {namen[paar % len(namen)]} und "
              f"{namen[(paar + 1) % len(namen)]}")

faceit.fenster_schliessen()
print()
print("  Zum Nachdenken:")
print("  Das Durchschnittsgesicht wirkt auf viele Menschen besonders")
print("  ebenmaessig. Woran koennte das liegen - und was heisst das fuer")
print("  Schoenheitsfilter, die genau in diese Richtung rechnen?")
print()
