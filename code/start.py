"""
Face it! - Startmenue.

Wenn du nicht jeden Befehl selbst tippen willst, starte dieses Menue.
Es fragt nur, welche Station du machen moechtest - und die Nummer im Menue
ist genau die Nummer der Station.

Starten:
    uv run code/start.py
    (oder unter Windows einfach start.bat doppelklicken)
"""

import subprocess
import sys
from pathlib import Path

import faceit

# Kennung, Datei, Emoji, Ersatzzeichen, Name, Beschreibung
STATIONEN = [
    ("0", "00_check.py", "🎥", "[K]",
     "Startcheck", "Läuft die Kamera?"),
    ("1", "01_pixel.py", "🔢", "[#]",
     "Station 1", "Ein Bild ist eine Tabelle"),
    ("2", "02_filter.py", "🧩", "[F]",
     "Station 2", "Filter und Faltung"),
    ("3", "03_detect.py", "🔍", "[?]",
     "Station 3", "Finde das Gesicht"),
    ("3b", "03b_landmarks.py", "✨", "[*]",
     "Station 3b", "Das Netz aus dem Logo"),
    ("4a", "04a_embedding.py", "👤", "[P]",
     "Station 4a", "Dein Gesicht als 128 Zahlen"),
    ("4b", "04b_vergleich.py", "🆚", "[=]",
     "Station 4b", "Wie ähnlich sind zwei Gesichter?"),
    ("4c", "04c_faceid.py", "🔓", "[U]",
     "Station 4c", "Deine eigene Handy-Entsperrung"),
    ("5", "05_bias.py", "📊", "[%]",
     "Station 5", "Fehler, Schwellen und Bias"),
    ("90", "90_anwesenheit.py", "📋", "[+]",
     "Advanced", "Anwesenheitsliste für die Tischgruppe"),
    ("91", "91_gesichtsraum.py", "🌌", "[o]",
     "Advanced", "Der 128-dimensionale Raum als Schatten"),
    ("92", "92_fehlerkurve.py", "📈", "[~]",
     "Advanced", "Die beiden Fehlerkurven zeichnen"),
    ("93", "93_durchschnitt.py", "👥", "[&]",
     "Advanced", "Gesichter mischen und mitteln"),
    ("94", "94_kernel_labor.py", "🧪", "[!]",
     "Advanced", "Eigener Kernel mit neun Reglern"),
    ("99", "99_cleanup.py", "🧹", "[X]",
     "Aufräumen", "Alle Gesichtsdaten löschen"),
]

# Nach diesen Kennungen kommt eine Trennlinie
TRENNER_NACH = {"0", "5", "94"}

HIER = Path(__file__).resolve().parent

# Welche Stationen wurden in dieser Sitzung schon gestartet?
erledigt = set()


def bildschirm_leeren():
    if faceit.FARBIG:
        print("\033[2J\033[H", end="")


def menue():
    breite = 62
    strich = "─" if faceit.EMOJI else "-"

    print()
    print("  " + faceit.bunt(strich * breite, "blau"))
    print("  " + faceit.bunt("Face it!", "blau", "fett")
          + faceit.bunt("   Computer Vision und Gesichtserkennung", "weiss"))
    print("  " + faceit.bunt(strich * breite, "blau"))
    print()

    for kennung, _, emoji, ersatz, name, beschreibung in STATIONEN:
        haken = (faceit.bunt(faceit.sym("✓", "x"), "gruen")
                 if kennung in erledigt else " ")
        zeile = ("   " + faceit.bunt(f"{kennung:<4}", "gelb", "fett")
                 + f"{faceit.sym(emoji, ersatz)}  "
                 + faceit.bunt(f"{name:<12}", "weiss")
                 + faceit.bunt(f"{beschreibung:<38}", "grau")
                 + f" {haken}")
        print(zeile.rstrip())
        if kennung in TRENNER_NACH:
            print("   " + faceit.bunt(strich * (breite - 1), "grau"))

    print()
    print("   " + faceit.bunt("q", "gelb", "fett") + "     beenden")
    print()


def starten(datei):
    print("   " + faceit.bunt(f"{faceit.sym('▶', '>')}  {datei} startet ...", "blau"))
    print()
    subprocess.run([sys.executable, str(HIER / datei)])


def farbtest():
    """
    Zeigt in zwei Sekunden, ob diese Konsole Farben und Emojis darstellt.
    Aufruf:  uv run code/start.py --farbtest
    """
    faceit.titel("Farb- und Emoji-Test",
                 f"Farben: {faceit.FARBIG}    Emojis: {faceit.EMOJI}")
    for stil in ("blau", "gruen", "rot", "gelb", "grau", "weiss"):
        print("   " + faceit.bunt(f"{stil:<8} so sieht das aus", stil))
    print()
    print("   Emojis: " + "  ".join(
        faceit.sym(emoji, ersatz) for _, _, emoji, ersatz, _, _ in STATIONEN))
    print()
    print("   Erwartet: bunte Zeilen und elf erkennbare Symbole.")
    print("   Kaestchen statt Symbolen? Dann starte über start.bat,")
    print("   oder schalte die Emojis ab:  set FACEIT_EMOJI=0")
    print("   Bunte Zeichenfolgen wie [96m? Dann:  set FACEIT_FARBEN=0")
    print()


if "--farbtest" in sys.argv:
    farbtest()
    sys.exit(0)

bildschirm_leeren()
kennungen = {kennung: datei for kennung, datei, *_ in STATIONEN}

while True:
    menue()
    eingabe = input("   " + faceit.bunt("Welche Station? ", "blau", "fett"))
    eingabe = eingabe.strip().lower().replace(" ", "")

    if eingabe in ("q", "quit", "exit", "ende", ""):
        print()
        print("   " + faceit.bunt("Bis dann.", "blau"))
        print()
        break

    if eingabe == "4":
        print()
        print("   " + faceit.bunt("Station 4 hat drei Teile: "
                                  "4a, 4b und 4c.", "gelb"))
        print("   Fang mit " + faceit.bunt("4a", "gelb", "fett") + " an.")
        input("\n   Enter drücken ")
        bildschirm_leeren()
        continue

    if eingabe not in kennungen:
        print()
        print("   " + faceit.bunt(f"{faceit.sym('🤔', '?')}  "
                                  f"'{eingabe}' kenne ich nicht.", "gelb"))
        print("   Möglich sind: "
              + ", ".join(k for k, *_ in STATIONEN) + " oder q")
        input("\n   Enter drücken ")
        bildschirm_leeren()
        continue

    starten(kennungen[eingabe])
    erledigt.add(eingabe)

    print()
    input("   " + faceit.bunt("Enter drücken für das Menü ", "grau"))
    bildschirm_leeren()
