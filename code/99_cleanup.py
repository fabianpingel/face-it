"""
Aufraeumen - alle Gesichtsdaten dieses Workshops loeschen.

Wir haben heute biometrische Daten von euch erzeugt: Fotos und
Zahlenvektoren, mit denen man euch identifizieren kann.
Die loeschen wir jetzt gemeinsam. Alle gleichzeitig.

Das ist keine Formalie. Genau das ist der Unterschied zwischen
"wir brauchen diese Daten" und "wir behalten diese Daten".
Die meisten Unternehmen tun das hier freiwillig nicht.

Starten:
    uv run code/99_cleanup.py
    uv run code/99_cleanup.py --ja      (ohne Rueckfrage)
"""

import shutil
import sys

import faceit

# Diese Ordner und Dateien enthalten Daten von euch
ZU_LOESCHEN = [
    ("fotos", "Fotos und Zahlengitter aus Station 1"),
    ("gesichter", "Gesichtsvektoren aus Station 4"),
    ("_test", "Testbilder"),
    ("faceid.npy", "deine gespeicherte Face ID"),
    ("anwesenheit.npz", "die Anwesenheitsliste"),
]

# Die Bildordner data/beispiele/ und data/personen/ stehen absichtlich NICHT
# in dieser Liste: das sind freie Bilder aus dem Netz und keine Daten von euch.
# Sie muessen das Loeschen ueberleben, sonst fehlen sie beim naechsten Termin.
# tests/test_6_personen.py haelt das fest.


def einsammeln():
    gefunden = []
    for name, beschreibung in ZU_LOESCHEN:
        pfad = faceit.DATEN / name
        if not pfad.exists():
            continue
        if pfad.is_dir():
            dateien = [d for d in pfad.rglob("*") if d.is_file()]
            groesse = sum(d.stat().st_size for d in dateien)
            gefunden.append((pfad, beschreibung, len(dateien), groesse))
        else:
            gefunden.append((pfad, beschreibung, 1, pfad.stat().st_size))
    return gefunden


faceit.titel("Aufraeumen", "Alle Gesichtsdaten dieses Workshops loeschen.")

gefunden = einsammeln()

if not gefunden:
    print("  Es ist nichts mehr zu loeschen. Alles schon sauber.")
    print()
    sys.exit(0)

anzahl_gesamt = sum(eintrag[2] for eintrag in gefunden)
bytes_gesamt = sum(eintrag[3] for eintrag in gefunden)

print("  Das wird geloescht:")
print()
for pfad, beschreibung, anzahl, groesse in gefunden:
    print(f"    {pfad.name:<20} {anzahl:4d} Datei(en)  "
          f"{groesse / 1024:8.1f} KB   {beschreibung}")
print()
print(f"  Zusammen: {anzahl_gesamt} Dateien, {bytes_gesamt / 1024:.1f} KB")
print()

if "--ja" not in sys.argv and not faceit.TESTMODUS:
    antwort = input('  Wirklich loeschen? Tippe "loeschen" und Enter: ')
    if antwort.strip().lower() != "loeschen":
        print()
        print("  Abgebrochen. Es wurde nichts geloescht.")
        print()
        sys.exit(0)

for pfad, _, _, _ in gefunden:
    if pfad.is_dir():
        shutil.rmtree(pfad)
    else:
        pfad.unlink()

print()
print(f"  {anzahl_gesamt} Dateien geloescht. Deine Gesichtsdaten sind weg.")
print()
print("  Zum Schluss eine Frage:")
print("  Wie viele Unternehmen, die dein Gesicht gespeichert haben,")
print("  haben so einen Knopf? Und wer drueckt ihn?")
print()
