"""
Face it! - Startmenue.

Wenn du nicht jeden Befehl selbst tippen willst, starte dieses Menue.
Es fragt nur, welche Station du machen moechtest.

Starten:
    uv run code/start.py
    (oder unter Windows einfach start.bat doppelklicken)
"""

import subprocess
import sys
from pathlib import Path

import faceit

STATIONEN = [
    ("00_check.py", "Startcheck", "Laeuft die Kamera?"),
    ("01_pixel.py", "Station 1", "Ein Bild ist eine Tabelle"),
    ("02_filter.py", "Station 2", "Filter und Faltung"),
    ("03_detect.py", "Station 3", "Finde das Gesicht"),
    ("03b_landmarks.py", "Station 3b", "468 Punkte (braucht MediaPipe)"),
    ("04_embedding.py", "Station 4a", "Dein Gesicht als 128 Zahlen"),
    ("05_vergleich.py", "Station 4b", "Wie aehnlich sind zwei Gesichter?"),
    ("06_faceid.py", "Station 4c", "Deine eigene Handy-Entsperrung"),
    ("08_bias.py", "Station 5", "Fehler, Schwellen und Bias"),
    ("07_bonus_anwesenheit.py", "Bonus", "Anwesenheitsliste"),
    ("99_cleanup.py", "Aufraeumen", "Alle Gesichtsdaten loeschen"),
]

HIER = Path(__file__).resolve().parent


def menue():
    print()
    print("  " + "=" * 58)
    print("  Face it!  -  Computer Vision und Gesichtserkennung")
    print("  " + "=" * 58)
    print()
    for nummer, (_, kurz, beschreibung) in enumerate(STATIONEN, start=1):
        print(f"    {nummer:2d}   {kurz:<12} {beschreibung}")
    print()
    print("     q   beenden")
    print()


while True:
    menue()
    eingabe = input("  Welche Station? ").strip().lower()

    if eingabe in ("q", "quit", "exit", ""):
        print()
        print("  Bis dann.")
        print()
        break

    if not eingabe.isdigit() or not 1 <= int(eingabe) <= len(STATIONEN):
        print(f"  Bitte eine Zahl zwischen 1 und {len(STATIONEN)} eingeben.")
        continue

    datei = STATIONEN[int(eingabe) - 1][0]
    print(f"  Starte {datei} ...")
    print()
    subprocess.run([sys.executable, str(HIER / datei)])
    print()
    input("  Enter druecken, um zum Menue zurueckzukehren ")
