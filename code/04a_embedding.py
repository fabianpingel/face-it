"""
Station 4a - Dein Gesicht als 128 Zahlen.

Bis jetzt weiss der Computer nur, WO ein Gesicht ist.
Jetzt kommt der eigentliche Trick der Gesichtserkennung.

Ein neuronales Netz schaut sich dein Gesicht an und schreibt
128 Zahlen auf. Immer 128, egal wer du bist.
Diese Zahlenliste nennt man einen Embedding-Vektor.

Das Besondere: Bei zwei Fotos derselben Person sind die 128 Zahlen
aehnlich. Bei zwei verschiedenen Personen sind sie unterschiedlich.
Mehr braucht Gesichtserkennung nicht.

Mach mindestens zwei Fotos von dir - du brauchst sie in Station 4b und 5.

Starten:
    uv run code/04a_embedding.py
    uv run code/04a_embedding.py Mia        (Name direkt mitgeben)
"""

import sys

import cv2
import numpy as np

import faceit

faceit.titel(
    "Station 4a - Dein Gesicht als 128 Zahlen",
    "[Leertaste] Foto machen und in Zahlen umrechnen",
    "[q] beenden",
)

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("  Wie sollen deine Aufnahmen heissen? (z. B. dein Vorname) ")
name = "".join(z for z in name.strip() if z.isalnum() or z in "-") or "ich"
print(f"  Aufnahmen werden gespeichert als: {name}_01, {name}_02, ...")
print()

detektor = faceit.detektor_laden()
erkenner = faceit.erkenner_laden()
kamera = faceit.kamera_oeffnen()
ordner = faceit.daten_ordner("gesichter")
zaehler = len(list(ordner.glob(f"{name}_*.npy")))

while True:
    bild = faceit.bild_holen(kamera)
    anzeige = bild.copy()
    gesichter = faceit.gesichter_finden(detektor, bild)

    for gesicht in gesichter:
        faceit.gesichtsrahmen(anzeige, gesicht, faceit.CYAN)

    if gesichter:
        faceit.schrift(anzeige, "Gesicht erkannt - Leertaste druecken",
                       (20, 46), faceit.CYAN, 0.8, 2)
    else:
        faceit.schrift(anzeige, "Kein Gesicht im Bild", (20, 46),
                       faceit.ROT, 0.8, 2)

    faceit.hinweisleiste(anzeige, ["[Leertaste] Foto machen", "[q] beenden"])
    faceit.zeigen("Face it - Station 4a", anzeige)

    gedrueckt = faceit.taste()
    if not faceit.fenster_offen("Face it - Station 4a"):
        break

    if gedrueckt == " ":
        if not gesichter:
            print("  Kein Gesicht im Bild - noch einmal versuchen.")
            continue

        # Falls mehrere Gesichter da sind: das groesste nehmen.
        gesicht = max(gesichter, key=lambda g: g[2] * g[3])

        # Das Gesicht wird gerade gedreht und auf 112 x 112 Pixel gebracht.
        ausgerichtet = erkenner.alignCrop(bild, gesicht)

        # Und jetzt der eigentliche Schritt: 112 x 112 Pixel werden zu 128 Zahlen.
        vektor = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)

        zaehler += 1
        np.save(ordner / f"{name}_{zaehler:02d}.npy", vektor)
        cv2.imwrite(str(ordner / f"{name}_{zaehler:02d}.png"), ausgerichtet)

        print()
        print(f"  Aufnahme {name}_{zaehler:02d} - das bist du in 128 Zahlen:")
        print()
        for i in range(0, 128, 8):
            print("   " + " ".join(f"{wert:+7.3f}" for wert in vektor[i:i + 8]))
        print()
        print(f"  Aus {ausgerichtet.shape[0]} x {ausgerichtet.shape[1]} x 3 "
              f"= {ausgerichtet.size} Zahlen wurden 128 Zahlen.")
        print("  Alles, was der Computer ueber dein Gesicht weiss, steht da oben.")
        print()

        gross = cv2.resize(ausgerichtet, (448, 448), interpolation=cv2.INTER_NEAREST)
        faceit.schrift(gross, f"{name}_{zaehler:02d}", (16, 34), faceit.CYAN, 0.8, 2)
        faceit.zeigen("Face it - so sieht das Modell dein Gesicht", gross)

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()

vorhanden = sorted(ordner.glob("*.npy"))
print(f"  Gespeicherte Gesichter insgesamt: {len(vorhanden)}")
if len(vorhanden) < 2:
    print("  Tipp: Mach noch ein zweites Foto - Station 4b braucht zwei.")
print()
print("  Weiter mit Station 4b: uv run code/04b_vergleich.py")
print()
