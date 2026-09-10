"""
Station 3b (Kuer) - Das Netz aus dem Workshop-Logo.

Ein zweites Modell legt 68 Punkte auf dein Gesicht: Augenwinkel, Nasenruecken,
Kinnlinie, Lippenrand. Diese Punkte werden dann zu Dreiecken verbunden -
und heraus kommt genau das Bild, das auf dem Logo dieses Workshops zu sehen ist.

Wichtig fuer das Verstaendnis:
Diese Punkte beschreiben nur die FORM deines Gesichts. Damit kann man Filter
bauen - Hundeohren, Sonnenbrille, Alterung. Aber man kann damit nicht
feststellen, WER du bist. Dafuer braucht es die 128 Zahlen aus Station 4.

Tasten:
    n   Netz oder nur Punkte
    q   beenden

Braucht einmalig ein weiteres Modell (54 MB):
    uv run code/tools/landmark_modell_holen.py
    uv run code/03b_landmarks.py

Fehlt das Modell, laeuft das Programm trotzdem und zeigt die fuenf Punkte
von YuNet. Es bricht nicht ab.
"""

import cv2
import numpy as np

import faceit

LANDMARK_MODELL = faceit.MODELLE / "lbfmodel.yaml"

# Fuer das Anpassen der 68 Punkte rechnen wir auf einem kleineren Bild -
# sonst ruckelt das Video.
ARBEITSBREITE = 640


def marker_laden():
    """
    Versucht, das Landmark-Modell zu laden.
    Gibt None zurueck, wenn etwas fehlt - dann laeuft die einfache Fassung.
    """
    if not hasattr(cv2, "face"):
        print("  Dieses OpenCV kennt das Modul cv2.face nicht.")
        print("  Erwartet wird opencv-contrib-python. Bitte 'uv sync' ausfuehren.")
        print()
        return None
    if not LANDMARK_MODELL.exists():
        print(f"  Das Landmark-Modell fehlt: {LANDMARK_MODELL}")
        print("  Holen mit:  uv run code/tools/landmark_modell_holen.py")
        print()
        return None
    marker = cv2.face.createFacemarkLBF()
    marker.loadModel(str(LANDMARK_MODELL))
    return marker


def punkte_finden(marker, bild, gesichter):
    """Gibt fuer jedes Gesicht die 68 Punkte zurueck."""
    hoehe, breite = bild.shape[:2]
    faktor = min(1.0, ARBEITSBREITE / breite)
    klein = cv2.resize(bild, None, fx=faktor, fy=faktor) if faktor < 1 else bild

    kaesten = np.array([[int(g[0] * faktor), int(g[1] * faktor),
                         int(g[2] * faktor), int(g[3] * faktor)]
                        for g in gesichter], dtype=np.int32)
    if len(kaesten) == 0:
        return []

    ok, marken = marker.fit(klein, kaesten)
    if not ok:
        return []
    return [np.array(m[0], dtype=np.float32) / faktor for m in marken]


def netz_zeichnen(bild, punkte, farbe=faceit.CYAN):
    """
    Verbindet die Punkte zu Dreiecken (Delaunay-Triangulation) und malt sie.
    Das ist derselbe Trick, mit dem Filter-Apps ein Gesicht verformen:
    Sie verschieben die Dreiecke.
    """
    hoehe, breite = bild.shape[:2]
    unterteilung = cv2.Subdiv2D((0, 0, breite, hoehe))
    for x, y in punkte:
        if 0 <= x < breite and 0 <= y < hoehe:
            unterteilung.insert((float(x), float(y)))

    for dreieck in unterteilung.getTriangleList():
        ecken = [(int(dreieck[0]), int(dreieck[1])),
                 (int(dreieck[2]), int(dreieck[3])),
                 (int(dreieck[4]), int(dreieck[5]))]
        if all(0 <= x < breite and 0 <= y < hoehe for x, y in ecken):
            cv2.polylines(bild, [np.array(ecken)], True, farbe, 1, cv2.LINE_AA)
    return bild


def punkte_zeichnen(bild, punkte):
    for x, y in punkte:
        cv2.circle(bild, (int(x), int(y)), 2, faceit.WEISS, -1, cv2.LINE_AA)
    return bild


faceit.titel(
    "Station 3b - Das Netz aus dem Logo",
    "68 Punkte auf deinem Gesicht, verbunden zu Dreiecken.",
    "[n] Netz oder nur Punkte     [q] beenden",
)

marker = marker_laden()
detektor = faceit.detektor_laden()
kamera = faceit.kamera_oeffnen()
netz_an = True

while True:
    bild = faceit.bild_holen(kamera)
    gesichter = faceit.gesichter_finden(detektor, bild)

    if marker is None:
        # Einfache Fassung: die fuenf Punkte, die YuNet mitliefert
        for gesicht in gesichter:
            faceit.gesichtsrahmen(bild, gesicht, faceit.CYAN)
        faceit.schrift(bild, "5 Punkte: Augen, Nase, Mundwinkel", (20, 46),
                       faceit.CYAN, 0.8, 2)
        faceit.schrift(bild, "Fuer 68 Punkte und das Netz:", (20, 84),
                       faceit.WEISS, 0.6, 1)
        faceit.schrift(bild, "uv run code/tools/landmark_modell_holen.py",
                       (20, 112), faceit.WEISS, 0.6, 1)
    else:
        alle_punkte = punkte_finden(marker, bild, gesichter)
        for punkte in alle_punkte:
            if netz_an:
                netz_zeichnen(bild, punkte)
            punkte_zeichnen(bild, punkte)

        faceit.schrift(bild, f"68 Punkte pro Gesicht  |  Gesichter: "
                             f"{len(alle_punkte)}", (20, 46), faceit.CYAN, 0.8, 2)
        faceit.schrift(bild, "Diese Punkte sagen, WIE dein Gesicht geformt ist -",
                       (20, 84), faceit.WEISS, 0.6, 1)
        faceit.schrift(bild, "nicht WER du bist.", (20, 112), faceit.WEISS, 0.6, 1)

    faceit.hinweisleiste(bild, ["[n] Netz oder Punkte   [q] beenden"])
    faceit.zeigen("Face it - Station 3b", bild)

    gedrueckt = faceit.taste()
    if gedrueckt == "q":
        break
    if gedrueckt == "n":
        netz_an = not netz_an
        print(f"  Darstellung: {'Dreiecksnetz' if netz_an else 'nur Punkte'}")

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 4: uv run code/04a_embedding.py")
print()
