"""
Station 1 - Ein Bild ist eine Tabelle.

Drueck die Leertaste und mach ein Foto von dir.
Das Programm rechnet dein Gesicht in ein Gitter aus Zahlen um
und schreibt diese Zahlen ins Terminal.

Jede Zahl sagt nur eines: wie hell ist dieser Punkt?
    0   = schwarz
    255 = weiss

Mehr weiss ein Computer ueber dein Gesicht an dieser Stelle nicht.

Starten:
    uv run code/01_pixel.py
"""

import cv2
import numpy as np

import faceit

# ======================================================================
#  HIER DARFST DU AENDERN
# ======================================================================

# Wie viele Pixel breit soll das Zahlengitter sein?
# Probiere: 8, 16, 32, 64
GROESSE = 16

# ======================================================================


def gitter_ausgeben(gitter):
    """Schreibt das Zahlengitter ins Terminal."""
    print()
    print("  Dein Gesicht als Zahlen:")
    print()
    for zeile in gitter:
        print("   " + " ".join(f"{int(wert):3d}" for wert in zeile))
    print()
    print(f"  Das sind {gitter.size} Zahlen. Das ist dein Gesicht fuer den Computer.")
    print()


def blatt_erzeugen(gitter, pfad):
    """
    Malt das Zahlengitter als Arbeitsblatt zum Ausdrucken.

    Die beiden Schwellen werden aus dem eigenen Bild berechnet (Drittel),
    damit das Ergebnis auch bei dunklen oder hellen Fotos gut aussieht.
    """
    dunkel = int(np.percentile(gitter, 33))
    hell = int(np.percentile(gitter, 66))

    zellen = gitter.shape[0]
    zelle = min(70, 1500 // zellen)
    rand = 60
    kopf = 120
    seite = np.full((zellen * zelle + 2 * rand + kopf,
                     zellen * zelle + 2 * rand, 3), 255, np.uint8)

    faceit.schrift(seite, "Face it!  -  Malen nach Zahlen", (rand, 46),
                   faceit.NAVY, 0.9, 2)
    faceit.schrift(seite, f"unter {dunkel}: ganz ausmalen   |   "
                          f"{dunkel} bis {hell}: schraffieren   |   "
                          f"ueber {hell}: frei lassen",
                   (rand, 78), faceit.NAVY, 0.52, 1)
    faceit.schrift(seite, "Was siehst du, wenn du fertig bist?",
                   (rand, 104), (120, 120, 120), 0.45, 1)

    for z in range(zellen):
        for s in range(zellen):
            x, y = rand + s * zelle, kopf + rand + z * zelle
            cv2.rectangle(seite, (x, y), (x + zelle, y + zelle),
                          (190, 190, 190), 1)
            wert = int(gitter[z, s])
            cv2.putText(seite, str(wert), (x + 8, y + zelle - 9),
                        cv2.FONT_HERSHEY_SIMPLEX, zelle / 145,
                        (110, 110, 110), 1, cv2.LINE_AA)

    cv2.imwrite(str(pfad), seite)
    return pfad


faceit.titel(
    "Station 1 - Ein Bild ist eine Tabelle",
    "[Leertaste] Foto machen     [q] beenden",
    f"Gitter: {GROESSE} x {GROESSE} Pixel  (oben im Code aenderbar)",
)

kamera = faceit.kamera_oeffnen()
fotos = faceit.daten_ordner("fotos")
zaehler = 0

def zielrahmen(bild):
    """
    Berechnet das Quadrat in der Bildmitte, in das das Gesicht gehoert.
    Nur dieser Bereich wird spaeter zu Zahlen umgerechnet - deshalb muss
    das Gesicht den Rahmen gut ausfuellen.
    """
    hoehe, breite = bild.shape[:2]
    kante = int(hoehe * 0.66)
    x = (breite - kante) // 2
    y = (hoehe - kante) // 2
    return x, y, kante


while True:
    bild = faceit.bild_holen(kamera)
    anzeige = bild.copy()

    x, y, kante = zielrahmen(bild)
    cv2.rectangle(anzeige, (x, y), (x + kante, y + kante), faceit.CYAN, 2)
    faceit.schrift(anzeige, "Gesicht in den Rahmen - moeglichst gross",
                   (x, y - 14), faceit.CYAN, 0.7, 2)
    faceit.hinweisleiste(anzeige, ["[Leertaste] Foto machen", "[q] beenden"])
    faceit.zeigen("Face it - Station 1", anzeige)

    gedrueckt = faceit.taste()

    if gedrueckt == " ":
        zaehler += 1

        # Schritt 1: Farben weg. Uebrig bleibt nur noch Helligkeit.
        grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)

        # Schritt 2: nur den Zielrahmen ausschneiden - also dein Gesicht.
        x, y, kante = zielrahmen(bild)
        grau = grau[y:y + kante, x:x + kante]

        # Schritt 3: klein rechnen - jetzt ist es ein Zahlengitter.
        gitter = cv2.resize(grau, (GROESSE, GROESSE),
                            interpolation=cv2.INTER_AREA)

        # ==============================================================
        #  EXPERIMENTE - nimm das Zeichen # vor einer Zeile weg
        # ==============================================================

        # Alles umdrehen: aus hell wird dunkel (Negativ)
        # gitter = 255 - gitter

        # Nur noch vier Helligkeitsstufen zulassen
        # gitter = gitter // 64 * 64

        # Alles heller machen (Achtung: ueber 255 geht nicht)
        # gitter = np.clip(gitter + 60, 0, 255).astype("uint8")

        # ==============================================================

        gitter_ausgeben(gitter)

        gross = cv2.resize(gitter, (560, 560), interpolation=cv2.INTER_NEAREST)
        gross = cv2.cvtColor(gross, cv2.COLOR_GRAY2BGR)
        faceit.schrift(gross, f"{GROESSE} x {GROESSE} Pixel", (16, 34),
                       faceit.CYAN, 0.8, 2)
        faceit.zeigen("Face it - dein Gesicht als Pixel", gross)

        original = cv2.resize(grau, (560, 560))
        cv2.imwrite(str(fotos / f"station1_{zaehler:02d}.png"),
                    np.hstack([cv2.cvtColor(original, cv2.COLOR_GRAY2BGR), gross]))

        blatt = blatt_erzeugen(gitter, fotos / f"malen_nach_zahlen_{zaehler:02d}.png")
        print(f"  Arbeitsblatt zum Ausdrucken: {blatt}")
        print()

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 2: uv run code/02_filter.py")
print()
