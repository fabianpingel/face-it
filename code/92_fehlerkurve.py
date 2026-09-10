"""
Advanced - Die Fehlerkurve zeichnen.

Station 5 zeigt eine Tabelle: Welche Schwelle macht wie viele Fehler?
Hier wird daraus ein Bild - zwei Kurven, die sich kreuzen.

    Falschabweisung (FRR)   Ich komme selbst nicht hinein.
                            Steigt, wenn die Schwelle steigt.
    Falschakzeptanz (FAR)   Ein Fremder kommt hinein.
                            Faellt, wenn die Schwelle steigt.

Der Punkt, an dem sich die Kurven kreuzen, hat einen Namen:
Equal Error Rate. Dort sind beide Fehler gleich haeufig.

Und genau hier sieht man, warum es keine perfekte Schwelle gibt:
Die eine Kurve steigt, die andere faellt. Man kann nur waehlen,
welchen Fehler man lieber macht.

Braucht die Aufnahmen aus Station 4a - mindestens zwei Personen und
mindestens ein Paar von zwei Bildern derselben Person.

Starten:
    uv run code/92_fehlerkurve.py
"""

from itertools import combinations

import cv2
import numpy as np

import faceit

BREITE, HOEHE = 960, 640
LINKS, RECHTS, OBEN, UNTEN = 90, 40, 70, 80


def paare_sammeln():
    """Vergleicht alle gespeicherten Gesichter paarweise."""
    ordner = faceit.daten_ordner("gesichter")
    dateien = sorted(ordner.glob("*.npy"))
    if len(dateien) < 4:
        faceit.abbruch(
            f"Es sind nur {len(dateien)} Gesichter gespeichert, "
            f"gebraucht werden mindestens 4.",
            "Nimm in Station 4a mehr Aufnahmen auf:",
            "   uv run code/04a_embedding.py Vorname",
        )

    vektoren = {pfad: np.load(pfad) for pfad in dateien}
    person = {pfad: (pfad.stem.rsplit("_", 1)[0] if "_" in pfad.stem
                     else pfad.stem) for pfad in dateien}

    gleiche, fremde = [], []
    for a, b in combinations(dateien, 2):
        wert = faceit.aehnlichkeit(vektoren[a], vektoren[b])
        (gleiche if person[a] == person[b] else fremde).append(wert)

    if not gleiche:
        faceit.abbruch(
            "Es gibt kein Paar von zwei Bildern DERSELBEN Person.",
            "Nimm von einer Person ein zweites Foto auf:",
            "   uv run code/04a_embedding.py Vorname",
        )
    if not fremde:
        faceit.abbruch(
            "Es sind Aufnahmen von nur einer Person gespeichert.",
            "Fuer die Falschakzeptanz braucht es mindestens zwei Personen.",
        )
    return gleiche, fremde


def kurven(gleiche, fremde, schritte=101):
    """
    Rechnet fuer jede Schwelle von 0 bis 1 die beiden Fehlerraten aus.
    FRR = Anteil der eigenen Paare, die abgewiesen werden.
    FAR = Anteil der fremden Paare, die akzeptiert werden.
    """
    schwellen = np.linspace(0.0, 1.0, schritte)
    frr = np.array([np.mean([w < s for w in gleiche]) for s in schwellen])
    far = np.array([np.mean([w >= s for w in fremde]) for s in schwellen])
    return schwellen, frr, far


def kreuzung(schwellen, frr, far):
    """Sucht die Schwelle, bei der beide Fehler etwa gleich gross sind."""
    index = int(np.argmin(np.abs(frr - far)))
    return schwellen[index], (frr[index] + far[index]) / 2


gleiche, fremde = paare_sammeln()
schwellen, frr, far = kurven(gleiche, fremde)
eer_schwelle, eer_wert = kreuzung(schwellen, frr, far)

faceit.titel(
    "Advanced - Die Fehlerkurve",
    f"{len(gleiche)} Paare derselben Person, {len(fremde)} fremde Paare",
    "[q] beenden",
)
print(f"  Kreuzungspunkt bei Schwelle {eer_schwelle:.2f} - "
      f"dort irren sich beide Seiten in {eer_wert * 100:.0f} Prozent der Faelle.")
print(f"  Das Modell selbst benutzt {faceit.SCHWELLE:.3f}.")
print()

# ---------------------------------------------------------------- zeichnen
tafel = np.full((HOEHE, BREITE, 3), 20, np.uint8)
plot_breite = BREITE - LINKS - RECHTS
plot_hoehe = HOEHE - OBEN - UNTEN


def auf_bild(schwelle, rate):
    return (int(LINKS + schwelle * plot_breite),
            int(OBEN + (1 - rate) * plot_hoehe))


# Gitternetz und Achsen
for anteil in np.arange(0, 1.01, 0.25):
    y = int(OBEN + (1 - anteil) * plot_hoehe)
    cv2.line(tafel, (LINKS, y), (LINKS + plot_breite, y), (48, 48, 48), 1)
    faceit.schrift(tafel, f"{anteil * 100:3.0f}%", (26, y + 5),
                   faceit.GRAU, 0.45, 1)
    x = int(LINKS + anteil * plot_breite)
    cv2.line(tafel, (x, OBEN), (x, OBEN + plot_hoehe), (48, 48, 48), 1)
    faceit.schrift(tafel, f"{anteil:.2f}", (x - 16, OBEN + plot_hoehe + 26),
                   faceit.GRAU, 0.45, 1)

# Die beiden Kurven
for werte, farbe, name in ((frr, faceit.ROT, "Falschabweisung FRR"),
                           (far, faceit.CYAN, "Falschakzeptanz FAR")):
    punkte = np.array([auf_bild(s, w) for s, w in zip(schwellen, werte)])
    cv2.polylines(tafel, [punkte], False, farbe, 2, cv2.LINE_AA)

# Kreuzungspunkt und die Schwelle des Modells
kreuz = auf_bild(eer_schwelle, eer_wert)
cv2.circle(tafel, kreuz, 8, faceit.WEISS, 2, cv2.LINE_AA)
faceit.schrift(tafel, f"Kreuzung bei {eer_schwelle:.2f}",
               (kreuz[0] + 16, max(OBEN + 20, kreuz[1] - 14)),
               faceit.WEISS, 0.5, 1)

x_modell = int(LINKS + faceit.SCHWELLE * plot_breite)  # gruene Linie
cv2.line(tafel, (x_modell, OBEN), (x_modell, OBEN + plot_hoehe),
         faceit.GRUEN, 1, cv2.LINE_AA)
faceit.schrift(tafel, f"Modell: {faceit.SCHWELLE:.3f}",
               (x_modell + 8, OBEN + 22), faceit.GRUEN, 0.5, 1)

# Beschriftung
faceit.schrift(tafel, "Zwei Fehler, eine Schwelle", (LINKS, 40),
               faceit.CYAN, 0.9, 2)
faceit.schrift(tafel, "Schwellenwert", (BREITE // 2 - 60, HOEHE - 26),
               faceit.GRAU, 0.55, 1)
# Legende in die Mitte: dort ist bei beiden Kurven meist Platz
legende_x = LINKS + int(plot_breite * 0.34)
for i, (farbe, name) in enumerate(((faceit.ROT, "FRR - ich komme nicht hinein"),
                                   (faceit.CYAN, "FAR - ein Fremder kommt hinein"))):
    y = OBEN + 40 + i * 28
    cv2.line(tafel, (legende_x, y - 5), (legende_x + 30, y - 5), farbe, 3)
    faceit.schrift(tafel, name, (legende_x + 40, y), faceit.WEISS, 0.5, 1)

ziel = faceit.daten_ordner("fotos") / "fehlerkurve.png"
cv2.imwrite(str(ziel), tafel)
print(f"  Bild gespeichert: {ziel}")
print()
print("  Zum Nachdenken:")
print("  Wo wuerdest du die gruene Linie hinschieben, wenn es um dein Handy")
print("  geht? Und wo, wenn eine Polizeikamera nach einem Verdaechtigen sucht?")
print()

while True:
    faceit.zeigen("Face it - Fehlerkurve", tafel)
    if faceit.taste(30) == "q" or not faceit.fenster_offen(
            "Face it - Fehlerkurve"):
        break

faceit.fenster_schliessen()
