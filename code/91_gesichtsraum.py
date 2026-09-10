"""
Advanced - Der 128-dimensionale Raum, sichtbar gemacht.

In Station 4 hast du gehoert: Dein Gesicht ist ein Punkt in einem Raum mit
128 Achsen. Das kann man nicht zeichnen. Aber man kann davon einen Schatten
machen - so wie ein dreidimensionaler Gegenstand einen zweidimensionalen
Schatten wirft.

Dieses Programm sucht die zwei Richtungen, in denen sich die Gesichter am
staerksten unterscheiden, und zeichnet alle Punkte in diese Ebene.
Das Verfahren heisst Hauptkomponentenanalyse (englisch PCA) und besteht
aus genau drei Schritten:

    1. Mittelwert abziehen  (alle Punkte um den Ursprung herum legen)
    2. Singulaerwertzerlegung  (die Hauptrichtungen finden)
    3. auf die ersten zwei Richtungen projizieren  (der Schatten)

Was du sehen wirst: Aufnahmen derselben Person liegen als Gruppe zusammen.
Genau darauf beruht Gesichtserkennung.

Braucht die Aufnahmen aus Station 4a. Je mehr Personen, desto schoener.

Starten:
    uv run code/91_gesichtsraum.py
"""

import cv2
import numpy as np

import faceit


def personen_farben(namen):
    """Gibt jeder Person eine eigene, gut unterscheidbare Farbe."""
    farben = {}
    for i, name in enumerate(sorted(namen)):
        ton = int(180 * i / max(1, len(namen)))
        farbe = cv2.cvtColor(np.uint8([[[ton, 200, 255]]]),
                             cv2.COLOR_HSV2BGR)[0][0]
        farben[name] = (int(farbe[0]), int(farbe[1]), int(farbe[2]))
    return farben


def hauptkomponenten(vektoren):
    """
    Projiziert die Vektoren auf ihre zwei Hauptrichtungen.
    Gibt die 2D-Punkte und den Anteil der erklaerten Streuung zurueck.
    """
    mitte = vektoren.mean(axis=0)
    zentriert = vektoren - mitte

    # Singulaerwertzerlegung: zentriert = U * S * V
    # Die Zeilen von V sind die Hauptrichtungen, S deren Gewicht.
    _, gewichte, richtungen = np.linalg.svd(zentriert, full_matrices=False)

    punkte = zentriert @ richtungen[:2].T
    anteil = (gewichte[:2] ** 2).sum() / (gewichte ** 2).sum()
    return punkte, anteil


faceit.titel(
    "Advanced - Der 128-dimensionale Raum als Schatten",
    "Hauptkomponentenanalyse der Gesichter aus Station 4a",
    "[q] beenden",
)

ordner = faceit.daten_ordner("gesichter")
dateien = sorted(ordner.glob("*.npy"))

if len(dateien) < 3:
    faceit.abbruch(
        f"Es sind nur {len(dateien)} Gesichter gespeichert, gebraucht werden 3.",
        "Nimm in Station 4a mehr Aufnahmen auf:",
        "   uv run code/04a_embedding.py Vorname",
    )

vektoren = np.array([np.load(pfad) for pfad in dateien], dtype=np.float64)
namen = [pfad.stem.rsplit("_", 1)[0] if "_" in pfad.stem else pfad.stem
         for pfad in dateien]

punkte, anteil = hauptkomponenten(vektoren)
farben = personen_farben(set(namen))

print(f"  {len(dateien)} Aufnahmen von {len(set(namen))} Person(en)")
print(f"  Die zwei gezeichneten Richtungen erklaeren "
      f"{anteil * 100:.0f} Prozent der Unterschiede.")
print(f"  Die restlichen {100 - anteil * 100:.0f} Prozent stecken in den "
      f"126 Richtungen, die hier fehlen.")
print()

# ---------------------------------------------------------------- zeichnen
BREITE, HOEHE, RAND = 900, 700, 70
tafel = np.full((HOEHE, BREITE, 3), 20, np.uint8)

# Punkte in Bildkoordinaten umrechnen
klein, gross = punkte.min(axis=0), punkte.max(axis=0)
spanne = np.maximum(gross - klein, 1e-9)


def auf_bild(punkt):
    rel = (punkt - klein) / spanne
    return (int(RAND + rel[0] * (BREITE - 2 * RAND)),
            int(HOEHE - RAND - rel[1] * (HOEHE - 2 * RAND)))


# Achsenkreuz durch den Mittelwert der Punkte
mitte = auf_bild(punkte.mean(axis=0))
cv2.line(tafel, (RAND, mitte[1]), (BREITE - RAND, mitte[1]), (55, 55, 55), 1)
cv2.line(tafel, (mitte[0], RAND), (mitte[0], HOEHE - RAND), (55, 55, 55), 1)

# Verbindungslinien zwischen Aufnahmen derselben Person
for name in set(namen):
    eigene = [i for i, n in enumerate(namen) if n == name]
    for i in eigene:
        for j in eigene:
            if i < j:
                cv2.line(tafel, auf_bild(punkte[i]), auf_bild(punkte[j]),
                         farben[name], 1, cv2.LINE_AA)

for i, name in enumerate(namen):
    ort = auf_bild(punkte[i])
    cv2.circle(tafel, ort, 9, farben[name], -1, cv2.LINE_AA)
    cv2.circle(tafel, ort, 9, (255, 255, 255), 1, cv2.LINE_AA)
    faceit.schrift(tafel, dateien[i].stem, (ort[0] + 14, ort[1] + 5),
                   faceit.WEISS, 0.45, 1)

faceit.schrift(tafel, "Der Gesichtsraum von oben", (RAND, 40),
               faceit.CYAN, 0.9, 2)
faceit.schrift(tafel, f"1. Hauptrichtung  ->", (BREITE - 300, HOEHE - 26),
               faceit.GRAU, 0.5, 1)
faceit.schrift(tafel, f"{len(dateien)} Aufnahmen  |  "
                      f"{len(set(namen))} Personen  |  "
                      f"{anteil * 100:.0f}% der Streuung sichtbar",
               (RAND, HOEHE - 26), faceit.GRAU, 0.5, 1)

# Legende
for i, name in enumerate(sorted(set(namen))):
    y = 80 + i * 26
    cv2.circle(tafel, (BREITE - 190, y - 5), 7, farben[name], -1, cv2.LINE_AA)
    faceit.schrift(tafel, name, (BREITE - 172, y), faceit.WEISS, 0.55, 1)

faceit.zeigen("Face it - Gesichtsraum", tafel)
ziel = faceit.daten_ordner("fotos") / "gesichtsraum.png"
cv2.imwrite(str(ziel), tafel)
print(f"  Bild gespeichert: {ziel}")
print()
print("  Zum Nachdenken:")
print("  Zwei Punkte koennen im Schatten nebeneinander liegen und in den")
print("  126 unsichtbaren Richtungen trotzdem weit auseinander sein.")
print("  Ein Schatten kann taeuschen - die Rechnung mit allen 128 Zahlen nicht.")
print()

while True:
    faceit.zeigen("Face it - Gesichtsraum", tafel)
    if faceit.taste(30) == "q" or not faceit.fenster_offen(
            "Face it - Gesichtsraum"):
        break

faceit.fenster_schliessen()
