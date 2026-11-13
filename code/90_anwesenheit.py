"""
Bonus - Anwesenheitsliste fuer deine Tischgruppe.

Melde mehrere Personen an und das Programm schreibt live die Namen
neben die Gesichter. Genau so funktionieren die Systeme, die manche
Firmen an ihren Eingaengen haben.

Waehrend du das baust, denk an eine Frage:
Wuerdest du wollen, dass deine Schule das im Klassenzimmer aufhaengt?

Tasten:
    n   neue Person anmelden (Name wird im Terminal eingegeben)
    l   Liste im Terminal anzeigen
    x   alle angemeldeten Personen loeschen
    q   beenden

Starten:
    uv run code/90_anwesenheit.py
"""

import numpy as np

import faceit

faceit.titel(
    "Bonus - Anwesenheitsliste",
    "[n] neue Person anmelden   [l] Liste   [x] leeren   [q] beenden",
)

detektor = faceit.detektor_laden()
erkenner = faceit.erkenner_laden()
kamera = faceit.kamera_oeffnen()
speicher = faceit.daten_ordner() / "anwesenheit.npz"

bekannte = {}
if speicher.exists():
    daten = np.load(speicher)
    bekannte = {name: daten[name] for name in daten.files}
    print(f"  {len(bekannte)} Person(en) waren schon angemeldet: "
          f"{', '.join(bekannte)}")
    print()


def sichern():
    if bekannte:
        np.savez(speicher, **bekannte)
    elif speicher.exists():
        speicher.unlink()


def wer_ist_das(vektor):
    """Sucht die aehnlichste angemeldete Person."""
    bester_name, bester_wert = None, -1.0
    for name, gespeichert in bekannte.items():
        wert = faceit.aehnlichkeit(vektor, gespeichert)
        if wert > bester_wert:
            bester_name, bester_wert = name, wert
    if bester_wert >= faceit.SCHWELLE:
        return bester_name, bester_wert
    return None, bester_wert


while True:
    bild = faceit.bild_holen(kamera)
    gesichter = faceit.gesichter_finden(detektor, bild)
    anwesend = set()

    for gesicht in gesichter:
        vektor = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
        name, wert = wer_ist_das(vektor)
        if name:
            anwesend.add(name)
            faceit.gesichtsrahmen(bild, gesicht, faceit.GRUEN,
                                  beschriftung=f"{name}  {wert * 100:.0f} %")
        else:
            faceit.gesichtsrahmen(bild, gesicht, faceit.ROT,
                                  beschriftung="unbekannt")

    faceit.schrift(bild, f"angemeldet: {len(bekannte)}   erkannt: "
                         f"{len(anwesend)}", (20, 46), faceit.AKZENT, 0.8, 2)
    for i, name in enumerate(sorted(bekannte)):
        farbe = faceit.GRUEN if name in anwesend else faceit.GRAU
        zeichen = "anwesend" if name in anwesend else "fehlt"
        faceit.schrift(bild, f"{name}: {zeichen}", (20, 90 + i * 30),
                       farbe, 0.65, 2)

    faceit.hinweisleiste(bild, ["[n] anmelden   [l] Liste   [x] leeren   [q] beenden"])
    faceit.zeigen("Face it - Anwesenheitsliste", bild)

    gedrueckt = faceit.taste()
    if not faceit.fenster_offen("Face it - Anwesenheitsliste"):
        break

    if gedrueckt == "n":
        if not gesichter:
            print("  Kein Gesicht im Bild.")
            continue
        gesicht = max(gesichter, key=lambda g: g[2] * g[3])
        name = input("  Name der Person: ").strip()
        name = "".join(z for z in name if z.isalnum() or z in "- ")
        if not name:
            print("  Kein Name eingegeben - abgebrochen.")
            continue
        bekannte[name] = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
        sichern()
        print(f"  {name} angemeldet. Jetzt sind es {len(bekannte)}.")

    elif gedrueckt == "l":
        print()
        print("  Angemeldete Personen:")
        for name in sorted(bekannte):
            print(f"    {name}  -  {'anwesend' if name in anwesend else 'fehlt'}")
        print()

    elif gedrueckt == "x":
        bekannte.clear()
        sichern()
        print("  Alle Anmeldungen geloescht.")

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print()
print("  Das war eine Ueberwachungsanlage in 120 Zeilen Python.")
print("  Denk an 99_cleanup.py, wenn du fertig bist.")
print()
