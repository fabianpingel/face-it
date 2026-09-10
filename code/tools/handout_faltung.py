"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Erzeugt das Arbeitsblatt B "Faltung von Hand":
    material/handouts/handout_B_faltung.html          (fuer die Klasse)
    material/handouts/handout_B_faltung_loesung.html  (fuer dich)

Zum Drucken die HTML-Datei im Browser oeffnen und Strg+P druecken.

Idee des Arbeitsblatts:
Ein winziges Bild (6 x 6 Felder) enthaelt eine senkrechte Kante: links
dunkel, rechts hell. Der Kernel wird von Hand darueber gelegt. Jede Gruppe
rechnet nur zwei Felder - eines in einer gleichmaessigen Flaeche und eines
auf der Kante. An der Tafel werden alle Ergebnisse zusammengesetzt:
In den Flaechen steht 0, auf der Kante eine grosse Zahl.

Damit man im Kopf rechnen kann, benutzen wir Helligkeiten von 0 bis 9
statt 0 bis 255. Am Prinzip aendert das nichts.

Die Zahlen im Arbeitsblatt und in der Loesung werden hier berechnet und
koennen deshalb nicht auseinanderlaufen.

Aufruf:
    uv run code/tools/handout_faltung.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

# Das kleine Bild: links dunkel (1), rechts hell (8).
# In der Mitte verlaeuft also eine senkrechte Kante.
BILD = np.array([
    [1, 1, 1, 8, 8, 8],
    [1, 1, 1, 8, 8, 8],
    [1, 1, 1, 8, 8, 8],
    [1, 1, 1, 8, 8, 8],
    [1, 1, 1, 8, 8, 8],
    [1, 1, 1, 8, 8, 8],
], dtype=int)

# Sobel-Kernel fuer senkrechte Kanten
KERNEL = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
], dtype=int)

ANZAHL_GRUPPEN = 8

STIL = """
  @page { size: A4 portrait; margin: 14mm; }
  * { box-sizing: border-box; }
  body { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
         color: #1a2b3c; margin: 0; font-size: 11.5pt; line-height: 1.5; }
  h1 { font-size: 20pt; margin: 0; color: #12263f; letter-spacing: -0.01em; }
  h1 span { color: #1ec8e6; }
  .unter { font-size: 12pt; color: #1ec8e6; margin: 2mm 0 0 0; font-weight: 600; }
  .linie { height: 3px; background: #1ec8e6; margin: 3mm 0 6mm 0; }
  h2 { font-size: 12pt; color: #12263f; margin: 0 0 3mm 0; }
  ol { margin: 2mm 0 0 0; padding-left: 6mm; }
  ol li { margin-bottom: 1.2mm; }
  .reihe { display: flex; gap: 12mm; align-items: flex-start; margin-bottom: 7mm; }
  table.gitter { border-collapse: collapse; }
  table.gitter td, table.gitter th { border: 1px solid #b9c2cc; width: 13mm;
        height: 13mm; text-align: center; vertical-align: middle;
        font-size: 13pt; font-variant-numeric: tabular-nums; }
  table.gitter th { border: none; color: #1ec8e6; font-size: 9.5pt;
        width: 8mm; height: 7mm; font-weight: 700; }
  table.gitter td.leer { background: #fbfdfe; }
  table.gruppen { border-collapse: collapse; font-size: 10.5pt; }
  table.gruppen td { padding: 0.8mm 4mm 0.8mm 0; }
  table.gruppen td.felder { color: #12263f; font-weight: 700;
        font-variant-numeric: tabular-nums; }
  .frage { color: #12263f; font-weight: 700; margin: 5mm 0 2mm 0; font-size: 12pt; }
  .klein { color: #63707d; font-size: 10pt; }
  .kasten { border-left: 3px solid #1ec8e6; padding: 2mm 0 2mm 4mm;
        margin: 4mm 0; background: #f5fcfe; }
  .loesung { color: #1ec8e6; font-weight: 700; }
"""


def falten(bild, kernel):
    """Rechnet die Faltung genau so, wie die Klasse sie von Hand rechnet."""
    hoehe, breite = bild.shape
    ergebnis = np.zeros((hoehe - 2, breite - 2), dtype=int)
    for z in range(hoehe - 2):
        for s in range(breite - 2):
            ergebnis[z, s] = int((bild[z:z + 3, s:s + 3] * kernel).sum())
    return ergebnis


def aufteilung(ergebnis, gruppen):
    """
    Verteilt die Ergebnisfelder so, dass jede Gruppe ein Feld aus einer
    gleichmaessigen Flaeche (Ergebnis 0) und ein Feld auf der Kante bekommt.
    Sonst rechnen manche Gruppen zweimal eine Null und erleben nichts.
    """
    felder = [(z, s) for z in range(ergebnis.shape[0])
              for s in range(ergebnis.shape[1])]
    kante = [f for f in felder if ergebnis[f] != 0]
    ruhig = [f for f in felder if ergebnis[f] == 0]

    verteilt = {}
    for i in range(gruppen):
        zuteilung = []
        if i < len(kante):
            zuteilung.append(kante[i])
        if i < len(ruhig):
            zuteilung.append(ruhig[i])
        verteilt[i + 1] = zuteilung

    # Falls mehr Felder als Gruppen da sind: den Rest gleichmaessig nachlegen.
    for i, feld in enumerate(kante[gruppen:] + ruhig[gruppen:]):
        verteilt[i % gruppen + 1].append(feld)
    return verteilt


def spaltenname(nummer):
    return chr(ord("A") + nummer)


def gitter_html(werte, zeigen=True, betrag=False, klasse=""):
    zeilen, spalten = werte.shape
    teile = [f'<table class="gitter {klasse}">']
    teile.append("<tr><th></th>" + "".join(
        f"<th>{spaltenname(s)}</th>" for s in range(spalten)) + "</tr>")
    for z in range(zeilen):
        teile.append(f"<tr><th>{z + 1}</th>")
        for s in range(spalten):
            if zeigen:
                wert = abs(werte[z, s]) if betrag else werte[z, s]
                teile.append(f"<td>{wert}</td>")
            else:
                teile.append('<td class="leer">&nbsp;</td>')
        teile.append("</tr>")
    teile.append("</table>")
    return "\n".join(teile)


def blatt(loesung=False):
    ergebnis = falten(BILD, KERNEL)
    verteilt = aufteilung(ergebnis, ANZAHL_GRUPPEN)

    gruppen_zeilen = "\n".join(
        f'<tr><td>Gruppe {nummer}</td><td class="felder">'
        + "&nbsp;&nbsp;&nbsp;".join(f"{z + 1}{spaltenname(s)}" for z, s in felder)
        + "</td></tr>"
        for nummer, felder in verteilt.items()
    )

    titel_zusatz = ' <span class="loesung">&middot; Lösung</span>' if loesung else ""

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Face it! – Arbeitsblatt B: Faltung von Hand</title>
<style>{STIL}</style>
</head>
<body>

<h1>Face it! <span>–</span> Arbeitsblatt B{titel_zusatz}</h1>
<p class="unter">Faltung von Hand</p>
<div class="linie"></div>

<p>Unten steht ein winziges Bild: 6 × 6 Helligkeitswerte. Damit man im Kopf
rechnen kann, gehen die Werte hier nur von 0 (dunkel) bis 9 (hell).
Am Prinzip ändert das nichts.</p>

<h2>So rechnest du ein Feld des Ergebnisses aus</h2>
<ol>
  <li>Lege den Kernel so auf das Bild, dass seine Mitte auf deinem Feld liegt.</li>
  <li>Multipliziere jede Kernel-Zahl mit der Bildzahl darunter.</li>
  <li>Addiere alle neun Ergebnisse.</li>
  <li>Schreibe den Betrag – also ohne Minuszeichen – in dein Feld.</li>
</ol>

<div class="reihe" style="margin-top:6mm">
  <div>
    <h2>Das Bild (6 × 6)</h2>
    {gitter_html(BILD)}
  </div>
  <div>
    <h2>Der Kernel (3 × 3)</h2>
    {gitter_html(KERNEL)}
    <h2 style="margin-top:7mm">Wer rechnet welche Felder?</h2>
    <table class="gruppen">{gruppen_zeilen}</table>
  </div>
</div>

<div class="reihe">
  <div>
    <h2>Das Ergebnis (4 × 4) – hier eintragen</h2>
    {gitter_html(ergebnis, zeigen=loesung, betrag=True)}
  </div>
  <div style="padding-top:9mm">
    <p>Wenn alle Gruppen fertig sind, werden die Zahlen an der Tafel
    zusammengesetzt.<br>Male jedes Feld an, in dem eine Zahl über 10 steht.</p>
    <p class="frage">Was ist zu sehen?<br>Und was hat der Kernel gefunden?</p>
  </div>
</div>

<div class="kasten">
  <p style="margin:0">Achte auf die Felder mit einer <strong>0</strong>: Dort war
  das Bild gleichmäßig hell oder gleichmäßig dunkel. Der Kernel interessiert sich
  nicht für Helligkeit – sondern nur für <strong>Veränderung</strong>.</p>
</div>

<p class="klein">Genau diese Rechnung machen die ersten Schichten eines neuronalen
Netzes – millionenfach pro Bild, mit tausenden Kerneln, die das Netz sich selbst
ausgedacht hat. Ihr habt einen davon von Hand gerechnet.</p>

</body>
</html>
"""


ziel = faceit.MATERIAL / "handouts"
ziel.mkdir(parents=True, exist_ok=True)

# Alte PNG-Fassungen entfernen, damit nicht zwei Versionen herumliegen
for alt in ziel.glob("handout_B_faltung*.png"):
    alt.unlink()

for mit_loesung in (False, True):
    name = ("handout_B_faltung_loesung.html" if mit_loesung
            else "handout_B_faltung.html")
    (ziel / name).write_text(blatt(mit_loesung), encoding="utf-8")
    print(f"  geschrieben: {ziel / name}")

ergebnis = falten(BILD, KERNEL)
print()
print("  Lösung – so sieht die Tafel am Ende aus:")
for zeile in np.abs(ergebnis):
    print("     " + "  ".join(f"{wert:3d}" for wert in zeile))
print()
print("  Aufteilung auf die Gruppen (jede bekommt eine Kante und eine Fläche):")
for nummer, felder in aufteilung(ergebnis, ANZAHL_GRUPPEN).items():
    felder_text = ", ".join(f"{z + 1}{spaltenname(s)}" for z, s in felder)
    werte = [abs(int(ergebnis[f])) for f in felder]
    print(f"     Gruppe {nummer}: {felder_text}  ->  {werte}")
print()
print("  Zum Drucken: HTML-Datei im Browser öffnen, Strg+P.")
print()
