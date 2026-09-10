"""
Station 2 - Filter und Faltung.

Ein Filter ist ein kleines Zahlengitter, ein sogenannter Kernel.
Der Kernel wandert ueber jedes Pixel deines Bildes. Ueberall multipliziert
er die Nachbarpixel mit seinen Zahlen und addiert alles zusammen.
Das Ergebnis ist der neue Wert des Pixels.

Genau das hast du eben auf dem Arbeitsblatt von Hand gerechnet.
Und genau das machen die ersten Schichten eines neuronalen Netzes -
nur mit tausenden Kerneln, die es sich selbst ausgedacht hat.

Starten:
    uv run code/02_filter.py
"""

import cv2
import numpy as np

import faceit

# ======================================================================
#  HIER DARFST DU AENDERN
# ======================================================================

# Dein eigener Kernel. Aendere die Zahlen und schau, was passiert.
KERNEL = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1],
]

# ======================================================================

# Fertige Kernel, umschaltbar mit den Zifferntasten
VORLAGEN = {
    "1": ("Original - macht nichts", [[0, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 0]]),
    "2": ("Weichzeichnen - Mittelwert", [[1 / 9, 1 / 9, 1 / 9],
                                         [1 / 9, 1 / 9, 1 / 9],
                                         [1 / 9, 1 / 9, 1 / 9]]),
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
    "0": ("Dein eigener Kernel (oben im Code)", KERNEL),
}


def anwenden(grau, kernel):
    """Legt den Kernel ueber jedes Pixel des Bildes."""
    kern = np.array(kernel, dtype=np.float32)
    ergebnis = cv2.filter2D(grau.astype(np.float32), -1, kern)
    # Negative Ergebnisse gibt es auch - wir zeigen ihren Betrag,
    # damit Kanten in beide Richtungen sichtbar werden.
    return np.clip(np.abs(ergebnis), 0, 255).astype(np.uint8)


def kernel_ins_bild(bild, kernel, name):
    """Zeichnet die neun Zahlen des Kernels sichtbar ins Bild."""
    faceit.schrift(bild, name, (16, 34), faceit.CYAN, 0.7, 2)
    for i, zeile in enumerate(kernel):
        text = "  ".join(f"{wert:5.2f}".rstrip("0").rstrip(".").rjust(5)
                          for wert in zeile)
        faceit.schrift(bild, text, (16, 70 + i * 30), faceit.WEISS, 0.6, 1)
    return bild


faceit.titel(
    "Station 2 - Filter und Faltung",
    "[0-6] Kernel umschalten     [q] beenden",
    "0 ist dein eigener Kernel aus dem Code.",
)
for taste_nr, (name, _) in VORLAGEN.items():
    print(f"    [{taste_nr}]  {name}")
print()

kamera = faceit.kamera_oeffnen()
aktuell = "4"

while True:
    bild = faceit.bild_holen(kamera)
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)

    name, kernel = VORLAGEN[aktuell]
    gefiltert = anwenden(grau, kernel)

    links = cv2.cvtColor(cv2.resize(grau, (560, 420)), cv2.COLOR_GRAY2BGR)
    rechts = cv2.cvtColor(cv2.resize(gefiltert, (560, 420)), cv2.COLOR_GRAY2BGR)
    faceit.schrift(links, "vorher", (16, 34), faceit.GRAU, 0.7, 2)
    kernel_ins_bild(rechts, kernel, name)

    zusammen = np.hstack([links, rechts])
    faceit.hinweisleiste(zusammen, ["[0-6] anderer Kernel", "[q] beenden"])
    faceit.zeigen("Face it - Station 2", zusammen)

    gedrueckt = faceit.taste()
    if gedrueckt == "q":
        break
    if gedrueckt in VORLAGEN:
        aktuell = gedrueckt
        print(f"  Kernel: {VORLAGEN[aktuell][0]}")
        for zeile in VORLAGEN[aktuell][1]:
            print("     " + "  ".join(f"{w:6.2f}" for w in zeile))
        summe = sum(sum(z) for z in VORLAGEN[aktuell][1])
        print(f"     Summe aller neun Zahlen: {summe:.2f}")
        print()

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 3: uv run code/03_detect.py")
print()
