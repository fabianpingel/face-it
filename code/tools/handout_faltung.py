"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Erzeugt das Arbeitsblatt B "Faltung von Hand":
    material/handouts/handout_B_faltung.html          (fuer die Klasse)
    material/handouts/handout_B_faltung_loesung.html  (fuer dich)

Zum Drucken die HTML-Datei im Browser oeffnen und Strg+P druecken.

Das Blatt hat zwei Seiten:

  Seite 1  erklaert die Rechnung an zwei vollstaendig ausgerechneten
           Beispielen mit farbigen Zahlen - einmal auf einer Kante,
           einmal auf einer gleichmaessigen Flaeche. Taugt auch als
           Vorlage fuer ein Tafelbild.
  Seite 2  ist die Aufgabe.

Idee der Aufgabe:
Ein winziges Bild (6 x 6 Felder) enthaelt eine senkrechte Kante: links
dunkel, rechts hell. Der Kernel wird von Hand darueber gelegt. Jede Gruppe
rechnet nur zwei Felder - eines in einer gleichmaessigen Flaeche und eines
auf der Kante. An der Tafel werden alle Ergebnisse zusammengesetzt:
In den Flaechen steht 0, auf der Kante eine grosse Zahl.

Auf dem Loesungsblatt steht zusaetzlich, WAS der Filter gefunden hat -
auf dem Aufgabenblatt bewusst nicht.

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

# Zwei Rechenbeispiele fuer die Erklaerseite. Bewusst andere Zahlen als in
# der Aufgabe (dort 1 und 8), damit die Loesung nicht verraten wird.
BEISPIEL_KANTE = np.array([[3, 3, 5],
                           [3, 3, 5],
                           [3, 3, 5]], dtype=int)

BEISPIEL_FLAECHE = np.array([[4, 4, 4],
                             [4, 4, 4],
                             [4, 4, 4]], dtype=int)

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

  /* Farben fuer das Rechenbeispiel: Kernelzahlen cyan, Bildzahlen dunkel */
  .kz { color: #0f8fa8; font-weight: 700; }
  .bz { color: #12263f; font-weight: 700; }
  table.gitter td.kern { color: #0f8fa8; font-weight: 700; }
  table.gitter td.bild { color: #12263f; font-weight: 700; }
  table.gitter td.treffer { background: #d4f1fa; font-weight: 700; }
  .rechnung { font-family: Consolas, "Courier New", monospace;
              font-size: 10pt; line-height: 1.9; margin: 2mm 0 0 0; }
  .rechnung .ergebnis { color: #0f8fa8; font-weight: 700; }
  .beispiel { border: 1px solid #cdd5dd; padding: 3mm 4mm; margin-bottom: 4mm; }
  .beispiel h3 { font-size: 11pt; color: #12263f; margin: 0 0 2mm 0; }
  .beispiel .zusammen { display: flex; gap: 5mm; align-items: center;
                        flex-wrap: wrap; }
  .mal { font-size: 16pt; color: #63707d; }
  .antwort { border-left: 3px solid #1ec8e6; background: #eefaff;
             padding: 3mm 0 3mm 4mm; margin: 4mm 0; }
  .antwort h3 { font-size: 11.5pt; color: #12263f; margin: 0 0 1.5mm 0; }
  .seitenwechsel { page-break-before: always; }
  .legende { font-size: 9.5pt; color: #63707d; margin-top: 1.5mm; }
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


def rechnung_html(bild, kernel):
    """
    Schreibt die Faltung eines einzigen Feldes Zeile fuer Zeile aus -
    mit farbigen Zahlen, damit klar ist, was womit multipliziert wird.
    Gibt (HTML, Gesamtsumme) zurueck.
    """
    def term(wert):
        """Negative Zahlen in Klammern - sonst stehen zwei Zeichen nebeneinander."""
        return f"({wert})" if wert < 0 else f"{wert}"

    zeilen, gesamt = [], 0
    for z in range(3):
        teile, produkte, summe = [], [], 0
        for s in range(3):
            k, b = int(kernel[z, s]), int(bild[z, s])
            summe += k * b
            teile.append(f'(<span class="kz">{k}</span> &middot; '
                         f'<span class="bz">{b}</span>)')
            produkte.append(term(k * b))
        gesamt += summe
        zeilen.append(" + ".join(teile)
                      + " &nbsp;=&nbsp; " + " + ".join(produkte)
                      + " &nbsp;=&nbsp; "
                      + f'<span class="ergebnis">{summe}</span>')
    zeilen.append('<span style="color:#63707d">Alle drei Zeilen addiert:</span>'
                  f' &nbsp;<span class="ergebnis">{gesamt}</span>'
                  f" &nbsp;&rarr;&nbsp; Betrag "
                  f'<span class="ergebnis">{abs(gesamt)}</span>')
    return '<p class="rechnung">' + "<br>".join(zeilen) + "</p>", gesamt


def gitter_html(werte, zeigen=True, betrag=False, klasse="",
                zellklasse="", treffer=False, kopf=True):
    """
    Baut ein Zahlengitter als HTML-Tabelle.

    zellklasse   faerbt alle Zahlen ("kern" cyan, "bild" dunkelblau)
    treffer      hebt Felder ungleich Null farbig hervor (fuer die Loesung)
    kopf         Spaltenbuchstaben und Zeilennummern anzeigen
    """
    zeilen, spalten = werte.shape
    teile = [f'<table class="gitter {klasse}">']
    if kopf:
        teile.append("<tr><th></th>" + "".join(
            f"<th>{spaltenname(s)}</th>" for s in range(spalten)) + "</tr>")
    for z in range(zeilen):
        teile.append("<tr>" + (f"<th>{z + 1}</th>" if kopf else ""))
        for s in range(spalten):
            if not zeigen:
                teile.append('<td class="leer">&nbsp;</td>')
                continue
            wert = abs(werte[z, s]) if betrag else werte[z, s]
            klassen = [zellklasse] if zellklasse else []
            if treffer and wert != 0:
                klassen.append("treffer")
            attribut = f' class="{" ".join(klassen)}"' if klassen else ""
            teile.append(f"<td{attribut}>{wert}</td>")
        teile.append("</tr>")
    teile.append("</table>")
    return "\n".join(teile)


def blatt(loesung=False):
    ergebnis = falten(BILD, KERNEL)
    verteilt = aufteilung(ergebnis, ANZAHL_GRUPPEN)

    gruppen_zeilen = chr(10).join(
        f'<tr><td>Gruppe {nummer}</td><td class="felder">'
        + "&nbsp;&nbsp;&nbsp;".join(f"{z + 1}{spaltenname(s)}" for z, s in felder)
        + "</td></tr>"
        for nummer, felder in verteilt.items()
    )

    rechnung_kante, summe_kante = rechnung_html(BEISPIEL_KANTE, KERNEL)
    rechnung_flaeche, summe_flaeche = rechnung_html(BEISPIEL_FLAECHE, KERNEL)

    titel_zusatz = ' <span class="loesung">&middot; Lösung</span>' if loesung else ""

    # Die Antwort steht nur auf dem Lösungsblatt.
    spalten_kante = [spaltenname(s) for s in range(ergebnis.shape[1])
                     if ergebnis[0, s] != 0]
    spalten_ruhig = [spaltenname(s) for s in range(ergebnis.shape[1])
                     if ergebnis[0, s] == 0]
    hoechster = int(abs(ergebnis).max())

    antwort = ""
    if loesung:
        antwort = f"""
<div class="antwort">
  <h3>Was hat der Filter gefunden?</h3>
  <p style="margin:0"><strong>Die senkrechte Kante in der Mitte des
  Bildes.</strong></p>
  <p style="margin:2mm 0 0 0">In den Spalten
  <strong>{" und ".join(spalten_kante)}</strong> steht überall
  <strong>{hoechster}</strong> – genau dort wechselt das Bild von dunkel (1)
  auf hell (8). In den Spalten <strong>{" und ".join(spalten_ruhig)}</strong>
  steht <strong>0</strong>, denn dort ist das Bild gleichmäßig: links dreimal
  die 1, rechts dreimal die 8.</p>
  <p style="margin:2mm 0 0 0">Angemalt ergeben die Felder über 10 einen
  <strong>senkrechten Streifen</strong> – an genau der Stelle, an der im Bild
  die Kante liegt. Der Filter hat also nicht die Helligkeit gemessen, sondern
  die <strong>Veränderung</strong> der Helligkeit.</p>
  <p style="margin:2mm 0 0 0; color:#63707d">Und deshalb ist die Summe der neun
  Kernelzahlen null: Ein Kantenfilter darf auf eine gleichmäßige Fläche nicht
  reagieren, egal wie hell sie ist.</p>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Face it! – Arbeitsblatt B: Faltung von Hand</title>
<style>{STIL}</style>
</head>
<body>

<h1>Face it! <span>–</span> Arbeitsblatt B{titel_zusatz}</h1>
<p class="unter">Faltung von Hand &nbsp;·&nbsp; Seite 1: So wird gerechnet</p>
<div class="linie"></div>

<p>Ein Filter ist ein kleines Zahlengitter, der <strong>Kernel</strong>. Er wird
über das Bild gelegt und liefert für jedes Feld eine neue Zahl. Auf Seite 2
rechnet ihr das für ein echtes Bild aus – hier steht erst einmal, <em>wie</em>
das geht.</p>

<div class="reihe" style="margin:4mm 0">
  <div>
    <h2>Der Kernel (3 × 3)</h2>
    {gitter_html(KERNEL, zellklasse="kern", kopf=False)}
    <p class="legende">Kernelzahlen sind <span class="kz">cyan</span>,
    Bildzahlen <span class="bz">dunkelblau</span>.</p>
  </div>
  <div>
    <h2>So rechnest du ein Feld aus</h2>
    <ol>
      <li>Lege den Kernel so auf das Bild, dass seine <strong>Mitte</strong>
          auf deinem Feld liegt.</li>
      <li>Multipliziere jede <span class="kz">Kernel-Zahl</span> mit der
          <span class="bz">Bildzahl</span>, die darunter liegt.</li>
      <li>Addiere alle neun Ergebnisse.</li>
      <li>Schreibe den <strong>Betrag</strong> – also ohne Minuszeichen –
          in dein Feld.</li>
    </ol>
  </div>
</div>

<div class="beispiel">
  <h3>Beispiel 1 &nbsp;·&nbsp; der Kernel liegt auf einer Kante</h3>
  <div class="zusammen">
    <div>
      {gitter_html(BEISPIEL_KANTE, zellklasse="bild", kopf=False)}
      <p class="legende">links dunkel (3), rechts hell (5)</p>
    </div>
    <div class="mal">&times;</div>
    <div>
      {gitter_html(KERNEL, zellklasse="kern", kopf=False)}
      <p class="legende">der Kernel</p>
    </div>
  </div>
  {rechnung_kante}
  <p style="margin:2mm 0 0 0">In das Feld kommt also die
  <strong>{abs(summe_kante)}</strong>.</p>
</div>

<div class="beispiel">
  <h3>Beispiel 2 &nbsp;·&nbsp; der Kernel liegt auf einer gleichmäßigen
  Fläche</h3>
  <div class="zusammen">
    <div>
      {gitter_html(BEISPIEL_FLAECHE, zellklasse="bild", kopf=False)}
      <p class="legende">überall dieselbe Helligkeit (4)</p>
    </div>
    <div class="mal">&times;</div>
    <div>
      {gitter_html(KERNEL, zellklasse="kern", kopf=False)}
      <p class="legende">derselbe Kernel</p>
    </div>
  </div>
  {rechnung_flaeche}
  <p style="margin:2mm 0 0 0">In das Feld kommt also die
  <strong>{abs(summe_flaeche)}</strong>.</p>
</div>

<div class="kasten">
  <p style="margin:0">Vergleicht die beiden Beispiele: dieselbe Rechnung, aber
  einmal kommt <strong>{abs(summe_kante)}</strong> heraus und einmal
  <strong>{abs(summe_flaeche)}</strong>. Merkt euch das – auf Seite 2 werdet ihr
  beide Fälle wiedersehen.</p>
</div>

<div class="seitenwechsel"></div>

<h1>Face it! <span>–</span> Arbeitsblatt B{titel_zusatz}</h1>
<p class="unter">Faltung von Hand &nbsp;·&nbsp; Seite 2: Eure Aufgabe</p>
<div class="linie"></div>

<p>Unten steht ein winziges Bild: 6 × 6 Helligkeitswerte. Damit man im Kopf
rechnen kann, gehen die Werte hier nur von 0 (dunkel) bis 9 (hell). Jede Gruppe
rechnet <strong>zwei Felder</strong> aus – genau so wie in den Beispielen auf
Seite 1.</p>

<div class="reihe" style="margin-top:5mm">
  <div>
    <h2>Das Bild (6 × 6)</h2>
    {gitter_html(BILD, zellklasse="bild")}
  </div>
  <div>
    <h2>Der Kernel (3 × 3)</h2>
    {gitter_html(KERNEL, zellklasse="kern", kopf=False)}
    <h2 style="margin-top:6mm">Wer rechnet welche Felder?</h2>
    <table class="gruppen">{gruppen_zeilen}</table>
  </div>
</div>

<div class="reihe">
  <div>
    <h2>Das Ergebnis (4 × 4) – hier eintragen</h2>
    {gitter_html(ergebnis, zeigen=loesung, betrag=True, treffer=loesung)}
  </div>
  <div style="padding-top:9mm">
    <p>Wenn alle Gruppen fertig sind, werden die Zahlen an der Tafel
    zusammengesetzt.<br>Male jedes Feld an, in dem eine Zahl über 10 steht.</p>
    <p class="frage">Was ist zu sehen?<br>Und was hat der Kernel gefunden?</p>
  </div>
</div>
{antwort}
<p class="klein">Genau diese Rechnung machen die ersten Schichten eines
neuronalen Netzes – millionenfach pro Bild, mit tausenden Kerneln, die das Netz
sich selbst ausgedacht hat. Ihr habt einen davon von Hand gerechnet.</p>

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
