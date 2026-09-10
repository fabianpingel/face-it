"""
Station 4c - Deine eigene Handy-Entsperrung.

So funktioniert Face ID:
  1. Einmal einrichten: ein Foto von dir wird zu 128 Zahlen und gespeichert.
  2. Danach bei jedem Blick in die Kamera: neue 128 Zahlen berechnen,
     mit den gespeicherten vergleichen.
  3. Ist die Aehnlichkeit groesser als die Schwelle, wird entsperrt.

Der Schieberegler oben im Fenster ist diese Schwelle.
Probiere in dieser Reihenfolge:

  Schwelle 36  -  es funktioniert
  Setz deine Nachbarin oder deinen Nachbarn davor  -  bleibt gesperrt
  Schwelle  5  -  jetzt entsperrt JEDER
  Schwelle 90  -  jetzt entsperrt NIEMAND, nicht mal du

Sicherheit ist keine Eigenschaft. Sicherheit ist eine Zahl,
die irgendein Mensch eingestellt hat.

Starten:
    uv run code/04c_faceid.py
"""

import cv2
import numpy as np

import faceit

FENSTER = "Face it - Station 4c: Face ID"
REGLER = "Schwelle in Prozent"

faceit.titel(
    "Station 4c - Deine eigene Handy-Entsperrung",
    "[e] Face ID einrichten (Foto von dir)",
    "[Schieberegler oben] Schwelle veraendern",
    "[q] beenden",
)

detektor = faceit.detektor_laden()
erkenner = faceit.erkenner_laden()
kamera = faceit.kamera_oeffnen()
speicher = faceit.daten_ordner() / "faceid.npy"

gespeicherter_vektor = None
if speicher.exists():
    gespeicherter_vektor = np.load(speicher)
    print(f"  Gespeicherte Face ID gefunden: {speicher}")
    print("  Mit [e] kannst du sie ueberschreiben.")
    print()

faceit.fenster(FENSTER)
faceit.regler_anlegen(FENSTER, REGLER, int(faceit.SCHWELLE * 100), 100)

while True:
    bild = faceit.bild_holen(kamera)
    schwelle = faceit.regler_wert(FENSTER, REGLER) / 100
    gesichter = faceit.gesichter_finden(detektor, bild)

    hoehe, breite = bild.shape[:2]
    bester_wert = None

    if gespeicherter_vektor is None:
        faceit.schrift(bild, "Noch nicht eingerichtet - druecke [e]",
                       (20, 50), faceit.CYAN, 0.9, 2)
        for gesicht in gesichter:
            faceit.gesichtsrahmen(bild, gesicht, faceit.GRAU)
    else:
        for gesicht in gesichter:
            vektor = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
            wert = faceit.aehnlichkeit(vektor, gespeicherter_vektor)
            offen = wert >= schwelle
            farbe = faceit.GRUEN if offen else faceit.ROT
            faceit.gesichtsrahmen(bild, gesicht, farbe,
                                  beschriftung=f"{wert * 100:.0f} %")
            if bester_wert is None or wert > bester_wert:
                bester_wert = wert

        offen = bester_wert is not None and bester_wert >= schwelle
        banner = "ENTSPERRT" if offen else "GESPERRT"
        farbe = faceit.GRUEN if offen else faceit.ROT

        streifen = bild[0:96, :].copy()
        cv2.rectangle(streifen, (0, 0), (breite, 96), farbe, -1)
        cv2.addWeighted(streifen, 0.85, bild[0:96, :], 0.15, 0, bild[0:96, :])
        faceit.schrift(bild, banner, (24, 68), (255, 255, 255), 1.8, 4)

        text = "kein Gesicht" if bester_wert is None else f"{bester_wert * 100:.0f} %"
        faceit.schrift(bild, f"Aehnlichkeit: {text}", (24, 140), faceit.WEISS, 0.8, 2)
        faceit.schrift(bild, f"Schwelle: {schwelle * 100:.0f} %",
                       (24, 176), faceit.CYAN, 0.8, 2)
        faceit.balken(bild, 0 if bester_wert is None else max(0.0, bester_wert),
                      (24, 196), 360, 24, farbe)
        x_schwelle = 24 + int(360 * schwelle)
        cv2.line(bild, (x_schwelle, 190), (x_schwelle, 226), faceit.WEISS, 2)

    faceit.hinweisleiste(bild, ["[e] neu einrichten   [q] beenden"])
    faceit.zeigen(FENSTER, bild)
    faceit.fenster_anpassen(FENSTER, bild)

    gedrueckt = faceit.taste()
    if not faceit.fenster_offen(FENSTER):
        break

    if gedrueckt == "e":
        if not gesichter:
            print("  Kein Gesicht im Bild - noch einmal versuchen.")
            continue
        gesicht = max(gesichter, key=lambda g: g[2] * g[3])
        gespeicherter_vektor = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
        np.save(speicher, gespeicherter_vektor)
        print(f"  Face ID eingerichtet und gespeichert in {speicher}")
        print("  Das sind 128 Zahlen in einer Datei. Nichts weiter.")
        print()

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print()
print("  Zum Nachdenken:")
print("  Bei welcher Schwelle wuerdest du dein Handy entsperren lassen?")
print("  Und bei welcher eine Banktuer? Und eine Polizeifahndung?")
print()
print("  Weiter mit Station 5: uv run code/05_bias.py")
print()
