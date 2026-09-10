"""
Startcheck - laeuft alles?

Dieses Programm zeigt einfach nur das Bild deiner Kamera.
Wenn du dich selbst siehst, ist dein Rechner bereit fuer den Workshop.

Starten:
    uv run code/00_check.py
"""

import sys

import faceit

faceit.titel(
    "Startcheck",
    "Wenn du dich selbst siehst, ist alles bereit.",
    "Zum Beenden auf das Bildfenster klicken und [q] druecken.",
)

# Wenn dein Rechner mehrere Kameras hat: uv run code/00_check.py 1
kamera_nummer = int(sys.argv[1]) if len(sys.argv) > 1 else 0
kamera = faceit.kamera_oeffnen(kamera_nummer)

while True:
    bild = faceit.bild_holen(kamera)

    hoehe, breite = bild.shape[:2]
    faceit.schrift(bild, "Es funktioniert!", (24, 60), faceit.CYAN, 1.4, 3)
    faceit.schrift(bild, f"Dein Bild ist {breite} x {hoehe} Pixel gross.",
                   (24, 105), faceit.WEISS, 0.75, 2)
    faceit.schrift(bild, f"Das sind {breite * hoehe:,} Zahlenwerte pro Farbe."
                   .replace(",", "."), (24, 140), faceit.WEISS, 0.75, 2)
    faceit.hinweisleiste(bild, ["[q] beenden"])

    faceit.zeigen("Face it - Startcheck", bild)
    if faceit.taste() == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print("  Startcheck bestanden. Weiter mit Station 1: uv run code/01_pixel.py")
print()
