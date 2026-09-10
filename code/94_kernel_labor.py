"""
Advanced - Das Kernel-Labor.

In Station 2 hast du fertige Kernel durchgeschaltet. Hier baust du deinen
eigenen: neun Schieberegler, einer fuer jede Zahl im 3 x 3-Gitter.

Die Regler gehen von -8 bis +8. Oben im Bild siehst du dein Gitter und
die Summe aller neun Zahlen. Diese Summe entscheidet ueber die Helligkeit:

    Summe = 1   Das Bild behaelt seine Helligkeit.
    Summe > 1   Das Bild wird heller.
    Summe < 1   Das Bild wird dunkler.
    Summe = 0   Die Helligkeit verschwindet ganz - uebrig bleibt nur,
                wo sich etwas AENDERT. Das ist ein Kantenfilter.

Aufgaben zum Ausprobieren:

    1. Baue einen Kernel, der nur senkrechte Kanten zeigt.
    2. Baue einen, der nur waagerechte Kanten zeigt.
    3. Baue einen, der das Bild nach rechts verschiebt.
    4. Finde einen Kernel, bei dem gar nichts passiert.
    5. Was macht ein Kernel, in dem nur eine einzige 1 steht,
       aber nicht in der Mitte?

Tasten:
    Schieberegler   die neun Zahlen des Kernels
    r               alle Regler zurueck auf den Ausgangswert
    s               Kernel ins Terminal schreiben
    q               beenden

Starten:
    uv run code/94_kernel_labor.py
"""

import cv2
import numpy as np

import faceit

FENSTER = "Face it - Kernel-Labor"

# Die Regler koennen keine negativen Zahlen. Deshalb laufen sie von
# 0 bis 16 und wir ziehen 8 ab: das ergibt -8 bis +8.
VERSCHIEBUNG = 8
HOECHSTWERT = 16
START = VERSCHIEBUNG + 0        # Regler starten bei 0

NAMEN = [f"{zeile}{spalte}" for zeile in "123" for spalte in "abc"]


def kernel_lesen():
    """Liest die neun Regler und baut daraus das 3 x 3-Gitter."""
    werte = [faceit.regler_wert(FENSTER, name) - VERSCHIEBUNG
             for name in NAMEN]
    return np.array(werte, dtype=np.float32).reshape(3, 3)


def anwenden(grau, kernel):
    ergebnis = cv2.filter2D(grau.astype(np.float32), -1, kernel)
    return np.clip(np.abs(ergebnis), 0, 255).astype(np.uint8)


def tafel_zeichnen(kernel):
    """Zeichnet das Kernel-Gitter und die Summe als Bildstreifen."""
    tafel = np.full((465, 260, 3), 22, np.uint8)
    summe = float(kernel.sum())

    faceit.schrift(tafel, "Dein Kernel", (18, 38), faceit.CYAN, 0.75, 2)

    zelle = 68
    for z in range(3):
        for s in range(3):
            x, y = 18 + s * zelle, 62 + z * zelle
            cv2.rectangle(tafel, (x, y), (x + zelle, y + zelle),
                          (70, 70, 70), 1)
            wert = int(kernel[z, s])
            farbe = (faceit.WEISS if wert == 0
                     else faceit.CYAN if wert > 0 else faceit.ROT)
            text = f"{wert:+d}" if wert else "0"
            breite = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX,
                                     0.7, 2)[0][0]
            faceit.schrift(tafel, text,
                           (x + (zelle - breite) // 2, y + zelle // 2 + 9),
                           farbe, 0.7, 2)

    y = 62 + 3 * zelle + 44
    faceit.schrift(tafel, f"Summe: {summe:+.0f}", (18, y), faceit.WEISS, 0.7, 2)

    if abs(summe - 1) < 0.01:
        deutung, farbe = "Helligkeit bleibt", faceit.GRUEN
    elif abs(summe) < 0.01:
        deutung, farbe = "Kantenfilter", faceit.CYAN
    elif summe > 1:
        deutung, farbe = "Bild wird heller", faceit.GELB
    else:
        deutung, farbe = "Bild wird dunkler", faceit.GRAU
    faceit.schrift(tafel, deutung, (18, y + 34), farbe, 0.6, 2)

    faceit.schrift(tafel, "[r] zuruecksetzen", (18, 400), faceit.GRAU, 0.5, 1)
    faceit.schrift(tafel, "[s] speichern", (18, 425), faceit.GRAU, 0.5, 1)
    faceit.schrift(tafel, "[q] beenden", (18, 450), faceit.GRAU, 0.5, 1)
    return tafel


faceit.titel(
    "Advanced - Das Kernel-Labor",
    "Neun Regler, ein Filter. Achte auf die Summe.",
    "[r] zuruecksetzen   [s] speichern   [q] beenden",
)

kamera = faceit.kamera_oeffnen()
faceit.fenster(FENSTER)
for name in NAMEN:
    faceit.regler_anlegen(FENSTER, name, START, HOECHSTWERT)

# Ein sinnvoller Startpunkt: die Mitte auf 1, alles andere auf 0.
# Das ist der Kernel, der nichts veraendert.
if not faceit.TESTMODUS:
    cv2.setTrackbarPos("2b", FENSTER, VERSCHIEBUNG + 1)

while True:
    bild = faceit.bild_holen(kamera)
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    kernel = kernel_lesen()

    links = cv2.cvtColor(cv2.resize(grau, (620, 465)), cv2.COLOR_GRAY2BGR)
    faceit.schrift(links, "vorher", (16, 34), faceit.GRAU, 0.7, 2)
    rechts = cv2.cvtColor(cv2.resize(anwenden(grau, kernel), (620, 465)),
                          cv2.COLOR_GRAY2BGR)
    faceit.schrift(rechts, "nachher", (16, 34), faceit.CYAN, 0.7, 2)

    ansicht = np.hstack([links, rechts, tafel_zeichnen(kernel)])
    faceit.zeigen(FENSTER, ansicht)
    faceit.fenster_anpassen(FENSTER, ansicht)

    gedrueckt = faceit.taste()
    if gedrueckt == "q":
        break
    if gedrueckt == "r" and not faceit.TESTMODUS:
        for name in NAMEN:
            cv2.setTrackbarPos(name, FENSTER, VERSCHIEBUNG)
        cv2.setTrackbarPos("2b", FENSTER, VERSCHIEBUNG + 1)
        print("  Zurueckgesetzt.")
    if gedrueckt == "s":
        print()
        print("  " + faceit.bunt("Dein Kernel:", "cyan", "fett"))
        for zeile in kernel.astype(int):
            print("     [" + ", ".join(f"{w:3d}" for w in zeile) + "],")
        print(f"     Summe: {kernel.sum():+.0f}")
        print()

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 3: uv run code/03_detect.py")
print()
