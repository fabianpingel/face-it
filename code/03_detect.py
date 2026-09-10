"""
Station 3 - Finde das Gesicht.

Dieses Programm sucht Gesichter im Kamerabild und malt einen Rahmen darum.
Aber Achtung: Es weiss nur, DASS da ein Gesicht ist.
Es hat keine Ahnung, WER du bist. Das ist Station 4.

Zwei Verfahren stehen zur Wahl:
  Haar-Cascade  aus dem Jahr 2001, sucht nach hell-dunkel-Mustern
  YuNet         ein neuronales Netz von 2023

Deine Aufgabe: Bring die Erkennung dazu, Fehler zu machen.
Halte ein Foto vor die Kamera. Dreh den Kopf. Zieh die Kapuze auf.
Zeig dem Programm eine Steckdose.

Starten:
    uv run code/03_detect.py
"""

import cv2

import faceit

FENSTER = "Face it - Station 3"

# ======================================================================
#  HIER DARFST DU AENDERN
# ======================================================================

# Wie gruendlich sucht die Haar-Cascade? Kleiner = gruendlicher und langsamer.
# Probiere 1.01 bis 1.5
SKALIERUNG = 1.1

# Wie viele Treffer muessen sich ueberlappen, damit es als Gesicht gilt?
# Kleiner = das Programm sieht ueberall Gesichter. Groesser = es sieht fast nichts.
# Probiere 1 bis 12
NACHBARN = 5

# ======================================================================

faceit.titel(
    "Station 3 - Finde das Gesicht",
    "[y] Verfahren umschalten (Haar / YuNet)",
    "[a] weniger streng    [d] strenger   (nur bei der Haar-Cascade)",
    "[q] beenden",
)

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
if cascade.empty():
    faceit.abbruch("Die Haar-Cascade konnte nicht geladen werden.",
                   "Bitte 'uv sync' ausfuehren.")

detektor = faceit.detektor_laden()
kamera = faceit.kamera_oeffnen()

yunet_an = False
nachbarn = NACHBARN

while True:
    bild = faceit.bild_holen(kamera)

    if yunet_an:
        verfahren = "YuNet (neuronales Netz, 2023)"
        gesichter = faceit.gesichter_finden(detektor, bild)
        for gesicht in gesichter:
            faceit.gesichtsrahmen(bild, gesicht, faceit.CYAN)
        anzahl = len(gesichter)
    else:
        verfahren = f"Haar-Cascade (2001), minNeighbors = {nachbarn}"
        grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
        treffer = cascade.detectMultiScale(
            grau, scaleFactor=SKALIERUNG, minNeighbors=nachbarn,
            minSize=(40, 40),
        )
        for (x, y, breite, hoehe) in treffer:
            cv2.rectangle(bild, (x, y), (x + breite, y + hoehe), faceit.GRUEN, 2)
        anzahl = len(treffer)

    faceit.schrift(bild, verfahren, (20, 44), faceit.CYAN, 0.75, 2)
    text = "kein Gesicht gefunden" if anzahl == 0 else (
        "1 Gesicht gefunden" if anzahl == 1 else f"{anzahl} Gesichter gefunden")
    faceit.schrift(bild, text, (20, 82),
                   faceit.WEISS if anzahl else faceit.ROT, 1.0, 2)
    # Die Regler fuer die Empfindlichkeit gehoeren zur Haar-Cascade.
    # YuNet hat sie nicht - dann verschwinden auch die Tastenhinweise,
    # damit niemand vergeblich darauf drueckt.
    if yunet_an:
        hinweise = ["[y] zurueck zur Haar-Cascade von 2001",
                    "[q] beenden"]
    else:
        hinweise = ["[y] YuNet ausprobieren   "
                    "[a] weniger streng   [d] strenger",
                    "[q] beenden"]
    faceit.hinweisleiste(bild, hinweise)
    faceit.zeigen(FENSTER, bild)

    gedrueckt = faceit.taste()
    if not faceit.fenster_offen(FENSTER):
        break
    if gedrueckt == "q":
        break
    if gedrueckt == "y":
        yunet_an = not yunet_an
        print(f"  Verfahren: {'YuNet' if yunet_an else 'Haar-Cascade'}")
    if gedrueckt == "a" and not yunet_an:
        nachbarn = max(1, nachbarn - 1)
        print(f"  minNeighbors = {nachbarn}  (weniger streng)")
    if gedrueckt == "d" and not yunet_an:
        nachbarn += 1
        print(f"  minNeighbors = {nachbarn}  (strenger)")

kamera.release()
faceit.fenster_schliessen()
print()
print("  Frage zum Mitnehmen:")
print("  Das Programm hat dein Gesicht gefunden. Weiss es, dass es DEIN Gesicht ist?")
print()
print("  Weiter mit Station 4: uv run code/04a_embedding.py")
print()
