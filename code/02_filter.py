"""
Station 2 - Filter und Faltung.

Ein Filter ist ein kleines Zahlengitter, ein sogenannter Kernel.
Der Kernel wandert ueber jedes Pixel deines Bildes. Ueberall multipliziert
er die Nachbarpixel mit seinen Zahlen und addiert alles zusammen.
Das Ergebnis ist der neue Wert des Pixels.

Genau das hast du eben auf Arbeitsblatt B von Hand gerechnet.
Und genau das machen die ersten Schichten eines neuronalen Netzes -
nur mit tausenden Kerneln, die es sich selbst ausgedacht hat.

Achte auf die Summe der Kernelzahlen. Sie steht mit im Bild:
    Summe = 1   Die Helligkeit bleibt. Weichzeichnen und Schaerfen.
    Summe = 0   Die Helligkeit verschwindet, uebrig bleibt nur die
                Veraenderung. Das ist ein Kantenfilter.

Tasten:
    0 bis 9   Kernel umschalten
    q         beenden

Tipp: Halte das Testmuster aus material/handouts/handout_F_testmuster.html
vor die Kamera. Dann siehst du genau, welche Kantenrichtung ein Kernel
findet - und welche er uebersieht.

Starten:
    uv run code/02_filter.py
"""

import cv2
import numpy as np

import faceit

# ======================================================================
#  HIER DARFST DU AENDERN  (Taste 0 zeigt diesen Kernel)
# ======================================================================

KERNEL = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1],
]

# ======================================================================


def mittelwert_kernel(kante):
    """Ein Kernel, der den Mittelwert aller Nachbarn bildet."""
    return (np.ones((kante, kante), np.float32) / (kante * kante)).tolist()


def bewegung_kernel(laenge):
    """Mittelwert nur nach links und rechts - sieht aus wie Verwackeln."""
    kern = np.zeros((laenge, laenge), np.float32)
    kern[laenge // 2, :] = 1 / laenge
    return kern.tolist()


# Fertige Kernel, umschaltbar mit den Zifferntasten
VORLAGEN = {
    "0": ("Dein eigener Kernel (oben im Code)", KERNEL),
    "1": ("Original - macht nichts", [[0, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 0]]),
    "2": ("Weichzeichnen - Mittelwert aus 25 Pixeln", mittelwert_kernel(5)),
    "3": ("Schaerfen", [[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]]),
    "4": ("Alle Kanten finden", [[-1, -1, -1],
                                 [-1, 8, -1],
                                 [-1, -1, -1]]),
    "5": ("Nur senkrechte Kanten (Sobel)", [[-1, 0, 1],
                                            [-2, 0, 2],
                                            [-1, 0, 1]]),
    "6": ("Nur waagerechte Kanten (Sobel)", [[-1, -2, -1],
                                             [0, 0, 0],
                                             [1, 2, 1]]),
    "7": ("Stark weichzeichnen - Mittelwert aus 81 Pixeln",
          mittelwert_kernel(9)),
    "8": ("Stark schaerfen", [[-1, -1, -1],
                              [-1, 9, -1],
                              [-1, -1, -1]]),
    "9": ("Bewegungsunschaerfe - Mittelwert nur nach links und rechts",
          bewegung_kernel(9)),
}


def anwenden(grau, kernel):
    """
    Legt den Kernel ueber jedes Pixel des Bildes.

    Bei Kantenfiltern (Summe 0) nehmen wir den Betrag - sonst waeren
    Kanten in einer der beiden Richtungen unsichtbar, weil sie negative
    Werte liefern. Bei allen anderen Kerneln schneiden wir nur oben und
    unten ab, damit das Bild natuerlich aussieht.
    """
    kern = np.array(kernel, dtype=np.float32)
    ergebnis = cv2.filter2D(grau.astype(np.float32), -1, kern)
    if abs(float(kern.sum())) < 0.01:
        ergebnis = np.abs(ergebnis)
    return np.clip(ergebnis, 0, 255).astype(np.uint8)


def kernel_beschreiben(kernel):
    """Gibt die Zeilen zurueck, die den Kernel im Bild beschreiben."""
    kern = np.array(kernel, dtype=np.float32)
    zeilen = []

    if kern.shape == (3, 3):
        for zeile in kern:
            zeilen.append("  ".join(f"{wert:5.2f}".rstrip("0").rstrip(".")
                                    .rjust(5) for wert in zeile))
    else:
        # Grosse Kernel passen nicht ins Bild - also beschreiben wir sie.
        einzelwerte = np.unique(np.round(kern, 4))
        zeilen.append(f"{kern.shape[0]} x {kern.shape[1]} = "
                      f"{kern.size} Zahlen")
        if len(einzelwerte) == 1:
            zeilen.append(f"alle Werte 1/{kern.size}")
        else:
            zeilen.append("nur eine Zeile ist besetzt")

    summe = float(kern.sum())
    if abs(summe - 1) < 0.01:
        deutung = "Helligkeit bleibt"
    elif abs(summe) < 0.01:
        deutung = "Kantenfilter"
    elif summe > 1:
        deutung = "wird heller"
    else:
        deutung = "wird dunkler"
    zeilen.append(f"Summe {summe:+.2f}  ->  {deutung}")
    return zeilen


def kernel_ins_bild(bild, kernel, name):
    """Schreibt Name, Zahlen und Summe des Kernels ins Bild."""
    faceit.schrift(bild, name, (16, 34), faceit.AKZENT, 0.62, 2)
    for i, zeile in enumerate(kernel_beschreiben(kernel)):
        farbe = faceit.GELB if zeile.startswith("Summe") else faceit.WEISS
        faceit.schrift(bild, zeile, (16, 70 + i * 30), farbe, 0.58, 1)
    return bild


faceit.titel(
    "Station 2 - Filter und Faltung",
    "[0-9] Kernel umschalten     [q] beenden",
    "Taste 0 zeigt deinen eigenen Kernel aus dem Code.",
)
for taste_nr in sorted(VORLAGEN):
    print(f"    [{taste_nr}]  {VORLAGEN[taste_nr][0]}")
print()

kamera = faceit.kamera_oeffnen()
aktuell = "4"

FENSTER = "Face it - Station 2"
faceit.fenster(FENSTER)

while True:
    bild = faceit.bild_holen(kamera)
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)

    name, kernel = VORLAGEN[aktuell]
    gefiltert = anwenden(grau, kernel)

    hoehe = 465
    faktor = hoehe / grau.shape[0]
    breite = int(grau.shape[1] * faktor)

    links = cv2.cvtColor(cv2.resize(grau, (breite, hoehe)), cv2.COLOR_GRAY2BGR)
    rechts = cv2.cvtColor(cv2.resize(gefiltert, (breite, hoehe)),
                          cv2.COLOR_GRAY2BGR)
    faceit.schrift(links, "vorher", (16, 34), faceit.GRAU, 0.7, 2)
    kernel_ins_bild(rechts, kernel, name)

    zusammen = np.hstack([links, rechts])
    faceit.hinweisleiste(zusammen, ["[0-9] anderer Kernel      [q] beenden"])
    faceit.zeigen(FENSTER, zusammen)
    faceit.fenster_anpassen(FENSTER, zusammen)

    gedrueckt = faceit.taste()
    if not faceit.fenster_offen(FENSTER):
        break
    if gedrueckt == "q":
        break
    if gedrueckt in VORLAGEN:
        aktuell = gedrueckt
        print(f"  [{aktuell}]  " + faceit.bunt(VORLAGEN[aktuell][0],
                                               "blau", "fett"))
        for zeile in kernel_beschreiben(VORLAGEN[aktuell][1]):
            print("       " + zeile)
        print()

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 3: uv run code/03_detect.py")
print()
