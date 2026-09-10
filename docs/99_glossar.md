# Glossar

Alle Begriffe, die im Workshop vorkommen – in der Reihenfolge, in der man ihnen
begegnet. Absichtlich in Alltagssprache erklärt, nicht in Fachsprache.

---

## Bild und Pixel

**Pixel**
Der kleinste Punkt eines digitalen Bildes. Ein Handyfoto hat mehrere Millionen
davon. Ein Pixel ist nichts als eine Zahl (oder drei, bei Farbe).

**Graustufe**
Die Helligkeit eines Pixels, angegeben als Zahl von 0 bis 255. 0 ist schwarz,
255 ist weiß, 128 ist mittelgrau. Warum bis 255? Weil eine Zahl bis 255 in
genau einem Byte Platz hat.

**Farbkanäle (RGB)**
Ein Farbbild besteht aus drei Zahlengittern übereinander: Rot, Grün, Blau. Aus
ihrer Mischung entsteht jede Farbe. Ein Farbpixel sind also drei Zahlen.
OpenCV speichert sie in der Reihenfolge Blau, Grün, Rot – eine Eigenheit, über
die viele stolpern.

**Auflösung**
Wie viele Pixel ein Bild breit und hoch ist, zum Beispiel 1280 × 720. Mehr
Auflösung heißt mehr Zahlen, nicht automatisch mehr Information.

**Matrix**
Der mathematische Name für ein Zahlengitter. Ein Graustufenbild *ist* eine
Matrix. Das ist der Grund, warum Bildverarbeitung Rechnen ist.

---

## Filter

**Kernel** (auch: Filtermaske)
Ein kleines Zahlengitter, meist 3 × 3, das über ein Bild gelegt wird. Seine
Zahlen bestimmen, worauf der Filter reagiert.

**Faltung** (englisch *convolution*)
Der Vorgang selbst: Kernel auf ein Pixel legen, jede Kernelzahl mit der Bildzahl
darunter multiplizieren, alles addieren, Ergebnis eintragen, ein Pixel weiter.
Genau das rechnet Arbeitsblatt B von Hand.

**Kantenfilter**
Ein Kernel, dessen Zahlen sich zu 0 addieren. Er reagiert deshalb nicht auf
Helligkeit, sondern nur auf *Veränderung* – also auf Kanten. Bekannte Beispiele
sind der Sobel-Filter und der Laplace-Filter.

**Weichzeichnen**
Ein Kernel, der den Mittelwert der Nachbarpixel bildet. Kleine Unterschiede
verschwinden, das Bild wird unscharf.

---

## Erkennen

**Gesichtsdetektion**
Die Frage: *Ist hier ein Gesicht, und wo?* Ergebnis ist ein Rechteck. Über die
Person sagt sie nichts.

**Gesichtserkennung**
Die Frage: *Wessen Gesicht ist das?* Dafür braucht man einen Vergleich mit
gespeicherten Gesichtern. Erst hier entstehen personenbezogene Daten.

**Haar-Cascade**
Ein Verfahren von 2001 (Viola und Jones). Es sucht nach einfachen Hell-Dunkel-
Mustern: Augenregion dunkler als Wangen, Nasenrücken heller als Nasenseiten.
Sehr schnell, leicht zu täuschen, findet Gesichter nur von vorn.

**YuNet**
Ein kleines neuronales Netz von 2023, das Gesichter findet. Robuster als die
Haar-Cascade, erkennt auch schräge Gesichter und liefert fünf Punkte mit:
beide Augen, Nasenspitze, zwei Mundwinkel.

**Landmarks**
Markante Punkte im Gesicht: Augenwinkel, Nasenrücken, Kinnlinie, Lippenrand.
YuNet liefert 5, das Modell in Station 3b liefert 68. Sie beschreiben die *Form*
eines Gesichts – nicht die Identität. Damit baut man Filter, keine Erkennung.

**Delaunay-Triangulation**
Ein Verfahren, das eine Punktwolke so zu Dreiecken verbindet, dass möglichst
gleichmäßige Dreiecke entstehen. Aus den 68 Landmarks wird damit das Netz aus dem
Workshop-Logo. Filter-Apps verformen genau diese Dreiecke, um ein Gesicht zu
verändern.

**Pareidolie**
Die menschliche Neigung, in Steckdosen, Autofronten und Wolken Gesichter zu
sehen. Software hat dasselbe Problem, aus einem ähnlichen Grund: Sie sucht nach
Mustern und findet sie auch dort, wo keine Absicht dahintersteckt.

---

## Der Kern: Zahlen statt Gesichter

**Embedding** (Merkmalsvektor)
Die 128 Zahlen, in die ein neuronales Netz ein Gesicht umrechnet. Aus 37 632
Zahlen (112 × 112 Pixel × 3 Farben) werden 128. Alles, was das Modell über ein
Gesicht behält, steht in dieser Liste.

**Vektor**
Eine Liste von Zahlen, verstanden als Punkt oder Pfeil in einem Raum. Zwei
Zahlen sind ein Punkt auf Papier, drei ein Punkt im Zimmer, 128 ein Punkt in
einem Raum, den man nicht zeichnen kann – aber rechnen kann man darin genauso.

**Kosinus-Ähnlichkeit**
Das Maß, mit dem zwei Embeddings verglichen werden: Zeigen die beiden Pfeile in
dieselbe Richtung? Ergebnis zwischen -1 und 1. Bei 1 sind sie identisch, bei 0
haben sie nichts miteinander zu tun.

**Schwellenwert**
Die Grenze, ab der ein Ähnlichkeitswert als „dieselbe Person" gilt. Beim hier
verwendeten Modell SFace liegt sie bei 0,363. Diese Zahl ist keine Naturkonstante,
sondern eine Entscheidung. Wer sie verschiebt, verschiebt die Fehler.

**SFace**
Das Modell, das im Workshop die 128 Zahlen berechnet. Es wurde mit Millionen
Gesichtsfotos trainiert.

**Training**
Der Vorgang, bei dem ein Netz seine Kernel und Gewichte selbst anpasst, bis es
seine Aufgabe erfüllt. Im Workshop trainieren wir nichts – wir benutzen fertig
trainierte Modelle. Das Training solcher Modelle dauert Tage auf teurer Hardware.

**ONNX**
Ein Dateiformat für trainierte neuronale Netze. Die Dateien in `models/` sind
genau das: eingefrorene Netze, die man laden und benutzen kann.

---

## Wenn es schiefgeht

**False Accept** (Falschakzeptanz)
Ein fremdes Gesicht wird als das eigene erkannt. Das Handy entsperrt für die
falsche Person. Der Fehler, der Sicherheit kostet.

**False Reject** (Falschabweisung)
Das eigene Gesicht wird nicht erkannt. Man kommt selbst nicht hinein. Der
Fehler, der Nerven kostet.

Diese beiden Fehler hängen zusammen wie zwei Enden einer Wippe: Wer den
Schwellenwert anhebt, senkt die Falschakzeptanz und erhöht die Falschabweisung.
Beide gleichzeitig auf null zu bringen, ist unmöglich.

**Spoofing**
Ein System mit einer Attrappe täuschen – ein Foto, ein Video, eine Maske.

**Liveness-Erkennung**
Die Gegenmaßnahme: prüfen, ob ein echter, lebender Mensch vor der Kamera ist.
Face ID auf dem iPhone projiziert dafür rund 30 000 Infrarotpunkte auf das
Gesicht und misst deren Abstände. Ein flaches Foto hat keine Tiefe und fällt
durch.

**Bias** (Verzerrung)
Wenn ein System bei bestimmten Menschengruppen systematisch mehr Fehler macht.
Ursache sind fast immer die Trainingsdaten: Wer darin selten vorkommt, wird
schlechter erkannt. Das Modell ist nicht böswillig, es ist einseitig gefüttert.

**Gender Shades**
Untersuchung von Joy Buolamwini und Timnit Gebru (MIT, 2018) an kommerziellen
Systemen zur Geschlechtsbestimmung. Fehlerrate bei hellhäutigen Männern: 0,8 %.
Bei dunkelhäutigen Frauen: 34,7 %. Dasselbe Programm.

**NIST FRVT**
Der große Vergleichstest von Gesichtserkennungssystemen durch eine
US-Bundesbehörde. Teil 3 von 2019 untersuchte 189 Algorithmen und fand bei vielen
davon 10- bis 100-mal höhere Falschtreffer-Raten für west- und ostafrikanische
sowie ostasiatische Gesichter im Vergleich zu osteuropäischen.

---

## Recht und Verantwortung

**Biometrische Daten**
Daten über körperliche Merkmale, mit denen eine Person eindeutig identifiziert
werden kann: Gesicht, Fingerabdruck, Iris, Stimme, Gangbild.

**DSGVO Artikel 9**
Die Datenschutz-Grundverordnung stuft biometrische Daten zur Identifizierung als
*besondere Kategorie* ein. Ihre Verarbeitung ist grundsätzlich verboten – erlaubt
nur mit ausdrücklicher Einwilligung oder in wenigen gesetzlich genannten Fällen.
Deshalb liegt diesem Workshop eine Einwilligung bei.

**EU AI Act**
Die KI-Verordnung der EU, seit 2024 in Kraft. Sie verbietet biometrische
Echtzeit-Fernidentifizierung im öffentlich zugänglichen Raum zu Zwecken der
Strafverfolgung grundsätzlich, mit engen Ausnahmen und richterlicher Genehmigung.
Ebenfalls verboten: das ungezielte Auslesen von Gesichtsbildern aus dem Internet
zum Aufbau von Datenbanken.

**Clearview AI**
Ein US-Unternehmen, das Milliarden Gesichtsfotos ungefragt aus sozialen Netzwerken
und dem offenen Netz gesammelt und eine Suchmaschine für Gesichter daraus gebaut
hat. Mehrere europäische Datenschutzbehörden haben dafür Bußgelder in
Millionenhöhe verhängt. Das Beispiel zeigt, wie wenig technischer Aufwand nötig
ist – und wie viel juristischer.

**Datensparsamkeit**
Der Grundsatz, nur die Daten zu erheben, die man wirklich braucht, und sie zu
löschen, sobald der Zweck erfüllt ist. Am Ende des Workshops führen wir das
mit `code/99_cleanup.py` gemeinsam aus.
