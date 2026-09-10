# Lösungen und erwartete Ergebnisse

Für die Lehrkraft. Alles, was die Schüler:innen herausfinden sollen – damit du
bei einer feststeckenden Gruppe in zehn Sekunden weiterhelfen kannst, statt selbst
zu suchen.

---

## Station 1 · Ein Bild ist eine Tabelle

**Erwartete Antworten auf dem Laufzettel**

| Frage | Antwort |
|---|---|
| Ab wie vielen Pixeln erkennt man, *dass* es ein Gesicht ist? | Erstaunlich wenige – bei rund **8 bis 12** Pixeln Kantenlänge sehen die meisten schon ein Gesicht. Grund: Augen, Nase und Mund erzeugen bereits bei sehr grober Auflösung ein charakteristisches Hell-Dunkel-Muster. Genau davon lebt die Haar-Cascade in Station 3. |
| Ab wie vielen Pixeln erkennt man, *wer* es ist? | Deutlich mehr, typisch **30 bis 60** – und stark abhängig davon, wie gut man die Person kennt. Bei Mitschüler:innen reicht oft weniger als erwartet. |

Der Regler hat elf feste Stufen: 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64. Feste
Werte deshalb, weil die Klasse hinterher über dieselben Zahlen reden soll.
| Was macht `gitter = 255 - gitter`? | Ein Negativ. Aus hell wird dunkel. Der Aha: Bildbearbeitung ist Rechnen mit Zahlen, nichts weiter. |

**Wenn nichts erkennbar ist:** Das Gesicht füllt den cyanfarbenen Zielrahmen nicht
aus. Näher an die Kamera, Licht von vorn, nicht im Gegenlicht sitzen.

**Bonus-Aufgaben**

- Einzelner Farbkanal: `grau = bild[:, :, 2]` nimmt nur Rot (OpenCV speichert BGR).
- Spiegeln: `gitter = gitter[:, ::-1]`
- Zwei Gesichter abziehen: `unterschied = abs(gitter_a.astype(int) - gitter_b.astype(int))`
  – große Werte dort, wo sich die Gesichter unterscheiden.

---

## Station 2 · Filter und Faltung

**Arbeitsblatt B (Faltung von Hand)**

Ergebnis der 4 × 4-Tabelle, Beträge:

```
 0   28   28    0
 0   28   28    0
 0   28   28    0
 0   28   28    0
```

Die Rechnung für ein Feld auf der Kante, zum Beispiel Zeile 1 / Spalte B:
Kernelmitte liegt über der Bildspalte C. Links stehen dreimal die 1, rechts
dreimal die 8.

```
(-1 · 1) + (0 · 1) + (1 · 8)
(-2 · 1) + (0 · 1) + (2 · 8)   =  7 + 14 + 7  =  28
(-1 · 1) + (0 · 1) + (1 · 8)
```

Und für ein Feld in der Fläche, zum Beispiel Zeile 1 / Spalte A: links und
rechts stehen dieselben Werte, die Summe ist genau **0**.

**Der entscheidende Satz:** Der Kernel reagiert nicht auf Helligkeit, sondern nur
auf *Veränderung* von Helligkeit. Deshalb steht in gleichmäßigen Flächen eine 0 –
egal ob die Fläche hell oder dunkel ist.

### Was hat der Filter gefunden?

Die Antwort, die auf dem Lösungsblatt steht und an der Tafel fallen soll:

> **Die senkrechte Kante in der Mitte des Bildes.** In den Spalten B und C steht
> überall 28 – genau dort wechselt das Bild von dunkel (1) auf hell (8). In den
> Spalten A und D steht 0, denn dort ist das Bild gleichmäßig. Angemalt ergibt
> das einen senkrechten Streifen an genau der Stelle, an der im Bild die Kante
> liegt.

Und die Anschlussfrage, falls jemand weiterdenkt: *Warum ist die Summe der neun
Kernelzahlen null?* Weil ein Kantenfilter auf eine gleichmäßige Fläche nicht
reagieren darf – egal wie hell sie ist.

### Testmuster: welcher Kernel findet welche Kante?

Gemessene Werte mit `handout_F_testmuster.html` vor der Kamera. „dunkel" heißt
exakt 0, „hell" heißt: die Kante ist als Linie deutlich zu sehen.

| Kernel | senkrecht | waagerecht | `/` | `\` |
|---|---|---|---|---|
| Taste 4 – alle Kanten | hell | hell | hell | hell |
| Taste 5 – senkrechte Kanten | **hell (max)** | **dunkel** | hell | hell |
| Taste 6 – waagerechte Kanten | **dunkel** | **hell (max)** | hell | hell |

Der Clou steckt nicht in der hellsten Spalte, sondern in der **dunklen**: Jeder
Richtungskernel ist für genau eine Richtung blind – nämlich für die, die
senkrecht zu seiner eigenen steht. Taste 4 dagegen ist überhaupt nicht
wählerisch, weil der Kernel in alle Richtungen gleich aufgebaut ist.

### Kernel-Challenge: die Diagonalen

Für die Diagonalen gibt es keinen Tastenpreset – das ist die eigentliche
Aufgabe. Die Klasse baut den Kernel mit `uv run code/94_kernel_labor.py`.

| Gesucht | Lösung | gemessen |
|---|---|---|
| Diagonale `/` findet, `\` blind | `[[0,1,2],[-1,0,1],[-2,-1,0]]` | `/` = 1020, `\` = **0** |
| Diagonale `\` findet, `/` blind | `[[2,1,0],[1,0,-1],[0,-1,-2]]` | `\` = 1020, `/` = **0** |

**Die Merkregel, auf die es hinausläuft:** Die Nullen im Kernel liegen immer
*entlang* der Kante, die er findet. Bei Taste 5 stehen sie als senkrechte Spalte
in der Mitte, bei Taste 6 als waagerechte Zeile – und für eine schräge Kante
müssen sie schräg liegen, also auf der Diagonale des Kernels.

Beide Lösungen haben Summe 0, sind also Kantenfilter. Andere Varianten gelten
auch: Es zählt allein, dass genau ein Testfeld völlig dunkel bleibt.

**Falls die Gruppen es nicht schaffen:** Es genügt, wenn sie *ausprobieren*, dass
die Nullen entlang der Kante liegen müssen. Die genauen Zahlen sind nicht das
Lernziel – der Zusammenhang zwischen Kernelaufbau und Richtung ist es.

### Weitere Fragen zu Station 2

| Frage | Antwort |
|---|---|
| Summe der neun Zahlen ungleich 1 | Ist die Summe **größer** als 1, wird das ganze Bild heller; ist sie **kleiner**, wird es dunkler. Bei Summe **0** bleibt nur die Veränderung übrig – das ist ein Kantenfilter. Das Programm schreibt die Summe und ihre Deutung mit ins Bild. |
| Warum ist Taste 2 (5 × 5) unschärfer als ein 3 × 3? | Weil über 25 statt über 9 Nachbarpixel gemittelt wird. Taste 7 mittelt über 81 – dort verschwinden auch die Gesichtszüge. |
| Was macht Taste 9? | Bewegungsunschärfe: Der Kernel mittelt nur nach links und rechts, nicht nach oben und unten. Sieht aus wie ein verwackeltes Foto. |
| Unterschied Taste 3 und Taste 8 | Beide schärfen und haben Summe 1, aber Taste 8 zieht deutlich stärker an. Bei zu starkem Schärfen entstehen helle Ränder – ein sichtbares Artefakt. |

**Häufiger Stolperstein:** Ein Kernel, dessen Zahlen sich zu einer großen Summe
addieren, liefert ein fast weißes Bild. Das ist kein Fehler, sondern die Antwort
auf die Frage nach der Summe.

---

## Station 3 · Finde das Gesicht

**Experimente-Bingo – was zu erwarten ist**

| Experiment | Haar-Cascade (2001) | YuNet (2023) |
|---|---|---|
| Kopf zur Seite drehen | verliert das Gesicht schon bei etwa **20 bis 30 Grad** | hält bis etwa **60 Grad** durch |
| Hand vor den Mund | findet es meist weiter | findet es weiter |
| Hand vor die Augen | **verliert** es sofort | verliert es meist |
| Sonnenbrille | oft verloren | meist gefunden |
| Licht aus / Gegenlicht | verliert es | robuster, aber irgendwann auch |
| **Foto auf dem Handy-Display** | **wird als Gesicht erkannt** | **wird ebenfalls erkannt** |
| Gesicht auf Kleidung, Poster, Zeichnung | wird häufig erkannt | wird erkannt, wenn es einem echten Gesicht ähnelt |
| Steckdose, Autofront | mit niedrigem `minNeighbors` erkannt | selten |
| Kapuze | funktioniert meist noch | funktioniert |
| Maske über Mund und Nase | oft verloren | meist gefunden |

Die wichtigste Zeile ist die mit dem Handy-Foto: **Detektion prüft nicht, ob ein
Mensch vor der Kamera sitzt.** Diese Beobachtung ist der Aufhänger für die
Hack-Challenge am Ende.

**Parameter drehen**

| Wert | Wirkung |
|---|---|
| `minNeighbors` = 1 oder 2 | Das Programm findet überall Gesichter: an der Wand, im Pullover, auf dem Tisch. Diese Fehltreffer heißen **False Positives**. |
| `minNeighbors` = 5 | Der Standardwert, brauchbarer Kompromiss. |
| `minNeighbors` ab etwa 12 | Fast nichts wird mehr gefunden, auch echte Gesichter nicht. |
| `SKALIERUNG` = 1.01 | Sehr gründlich, aber deutlich langsamer – das Bild ruckelt sichtbar. |
| `SKALIERUNG` = 1.5 | Schnell, übersieht aber viele Gesichter. |

**Antwort auf die Abschlussfrage:** Nein, das Programm weiß nicht, wer da ist. Es
hat nur ein Muster gefunden, das nach Gesicht aussieht. Für die Identität braucht
es Station 4 – und einen Vergleich mit gespeicherten Daten.

---

## Station 3b · Was kann man mit Landmarks bauen?

Die Aufgabe lautet: *Diese 68 Punkte sagen, wie ein Gesicht geformt ist – nicht,
wer es ist. Was könnte man damit bauen?* Zwei Minuten sammeln, dann an der Tafel
in zwei Spalten sortieren.

**Der Punkt, auf den es hinausläuft:** Alle diese Anwendungen funktionieren,
**ohne** dass jemand identifiziert wird. Landmarks beschreiben Form und
Bewegung, nicht Identität. Man kann also durchaus etwas Nützliches bauen, ohne
eine Gesichtsdatenbank anzulegen – das ist keine Selbstverständlichkeit,
sondern eine Entwurfsentscheidung.

### Spalte „nützlich"

| Idee | Wie es technisch geht |
|---|---|
| **Emotionen ablesen** | Mundwinkel oben oder unten, Augenbrauen hoch, Augen zusammengekniffen. Man misst nur Abstände zwischen Punkten. |
| **Lächel-Auslöser** | Die Kamera fotografiert erst, wenn alle Mundwinkel oben sind. Gibt es wirklich, heißt bei manchen Herstellern „Smile Shutter". |
| **Müdigkeitswarner im Auto** | Sind die Augen länger als etwa eine Sekunde geschlossen oder sinkt die Blinkfrequenz, kommt ein Warnton. In neu zugelassenen Fahrzeugtypen in der EU vorgeschrieben. |
| **Steuerung ohne Hände** | Kopfneigung und Blinzeln als Maus und Klick – für Menschen, die eine Tastatur nicht bedienen können. |
| **Filter und Masken** | Hundeohren, Sonnenbrille, virtuelles Make-up. Die Dreiecke des Netzes werden verzogen, das Bild verzieht sich mit. Genau das macht `93_durchschnitt.py` in einfacher Form. |
| **Brille online anprobieren** | Aus den Punkten am Nasenrücken und an den Augen ergibt sich, wie ein Gestell sitzen würde. |
| **Avatare animieren** | Memoji, Spielfiguren, Videokonferenz-Avatare: Die Punkte steuern das Gesicht einer Figur. |
| **Liveness-Prüfung** | „Bitte einmal blinzeln." Ein Foto blinzelt nicht – damit fällt genau der Angriff durch, den die Klasse in der Hack-Challenge fährt. |
| **Medizin und Pflege** | Schmerzerkennung bei Menschen, die nicht sprechen können. Verlaufskontrolle in der Kieferorthopädie. |
| **Sitzt die Maske? Sitzt die Schutzbrille?** | Prüfen, ob Mund und Nase bedeckt sind – ohne zu wissen, wer davorsteht. |

### Spalte „unheimlich"

| Idee | Warum sie unangenehm ist |
|---|---|
| **Aufmerksamkeitsmessung** | Schaut die Person auf den Bildschirm? Im Klassenzimmer oder im Büro eingesetzt, wird daraus eine Dauerkontrolle. |
| **Blickmessung in Geschäften** | Welches Regal wird wie lange betrachtet? Die Kundin weiß nichts davon. |
| **Prüfungsüberwachung** | Software, die beim Homeschooling Blickrichtung und Kopfbewegung protokolliert und „Verdachtsfälle" meldet. |
| **Emotionsanalyse im Bewerbungsgespräch** | Aus Mundwinkeln auf Eignung schließen. Fachlich zweifelhaft und rechtlich heikel. |

**Der harte Fakt für diese Spalte:** Der **EU AI Act verbietet** das Ableiten von
Emotionen aus biometrischen Daten **am Arbeitsplatz und in Bildungseinrichtungen**
– mit engen Ausnahmen für medizinische und Sicherheitszwecke. Der Gesetzgeber hat
also genau die Spalte „unheimlich" gesehen und einen Teil davon untersagt.

**Wenn die Diskussion Fahrt aufnimmt**, ist die weiterführende Frage: Woran
merkt man den Unterschied zwischen dem Müdigkeitswarner im Auto und der
Aufmerksamkeitsmessung im Klassenzimmer? Beide messen dasselbe. Der Unterschied
liegt nicht in der Technik, sondern darin, *wer* die Daten bekommt und *wozu*.
Diesen Satz kann man an der Tafel stehen lassen – er trägt bis in Block 5.

---

## Station 4 · Wer ist das?

**Typische Ähnlichkeitswerte** (SFace, Schwelle 0,363)

| Vergleich | Erwarteter Bereich |
|---|---|
| Ich – ich, gleiche Sitzung, gleiches Licht | **0,75 bis 0,95** |
| Ich – ich, Brille ab/auf, andere Frisur, Grimasse | **0,45 bis 0,75** |
| Ich – ich, sehr schlechtes Licht oder halb verdeckt | kann unter **0,363** fallen → Falschabweisung |
| Zwei verschiedene Personen | **-0,1 bis 0,25** |
| Geschwister oder Cousins | **0,2 bis 0,45** – hier wird es spannend, gelegentlich über der Schwelle |
| Ich – Portrait aus `data/beispiele` | nahe **0** |

**Wenn alle Werte sehr hoch sind:** Vermutlich wurden beide Aufnahmen im selben
Moment gemacht, also praktisch dasselbe Bild. Zwischen den Aufnahmen bewusst etwas
verändern.

**Station 4c – die Choreografie am Schieberegler**

| Schwelle | Ich selbst | Andere Person |
|---|---|---|
| 36 % (Standard) | entsperrt | bleibt gesperrt |
| 5 % | entsperrt | **entsperrt ebenfalls** – jeder kommt hinein |
| 90 % | **bleibt gesperrt** – nicht einmal ich selbst | bleibt gesperrt |

**Die Begriffe, erst hier:**

- **False Accept** – ein Fremder kommt hinein. Sinkt, wenn man die Schwelle anhebt.
- **False Reject** – ich komme selbst nicht hinein. Steigt, wenn man die Schwelle anhebt.

Beide gleichzeitig auf null zu bringen, ist unmöglich. Beim Handy ist eine
Falschabweisung nur ärgerlich, eine Falschakzeptanz aber ein Sicherheitsproblem –
deshalb liegt die Schwelle dort hoch. Bei einer Polizeifahndung ist es umgekehrt
brisant: Eine Falschakzeptanz trifft eine unschuldige Person.

---

## Station 5 · Fehler und Bias

`uv run code/05_bias.py` braucht mindestens vier gespeicherte Aufnahmen und
mindestens ein Paar derselben Person, sonst weist das Skript darauf hin.

**Was in Teil 1 herauskommt**

Die Verteilung „dieselbe Person" liegt hoch, die Verteilung „verschiedene
Personen" niedrig – aber die Bereiche **überlappen sich**, sobald schwierige
Aufnahmen dabei sind (schlechtes Licht, Brille, Kopf zur Seite). Genau das ist das
Ziel: Es gibt keine Schwelle, die alles richtig macht. Die Tabelle zeigt für jede
Schwelle die Summe beider Fehlerarten und markiert den Standardwert des Modells.

Wenn sich die Bereiche noch sauber trennen, fehlen schwierige Aufnahmen. Dann
zurück zu Station 4a und bewusst schlechte Bilder machen – das ist keine
Fehlbedienung, sondern die eigentliche Aufgabe.

**Zahlen für Teil 2, falls jemand nachfragt**

- **Gender Shades**, Buolamwini und Gebru, MIT 2018: drei kommerzielle Systeme zur
  *Geschlechtsbestimmung* aus Fotos. Fehlerrate 0,8 % bei hellhäutigen Männern,
  34,7 % bei dunkelhäutigen Frauen. Wichtig für die Genauigkeit: Das war
  Geschlechtsklassifikation, nicht Identifikation.
- **NIST FRVT Part 3**, 2019: 189 Algorithmen im Test. Bei der Verifikation zweier
  Gesichter lagen die Falschtrefferraten für west- und ostafrikanische sowie
  ostasiatische Gesichter bei vielen Algorithmen **10- bis 100-mal höher** als für
  osteuropäische.
- **Ursache** in beiden Fällen: die Zusammensetzung der Trainingsdaten.

---

## Hack-Challenge

| Angriff | Klappt er? | Warum |
|---|---|---|
| Foto auf dem Handy-Display | **ja**, sehr zuverlässig | Die Webcam sieht ein flaches Zahlengitter und kann Haut nicht von Glas unterscheiden. |
| Ausdruck auf Papier | **ja** | Gleicher Grund. Gut beleuchtet und nicht zu klein ausdrucken. |
| Video statt Foto | ja | Bringt gegenüber dem Foto nur dann etwas, wenn ein System Blinzeln prüft – unser Programm tut das nicht. |
| Ähnlich aussehende Person | manchmal | Geschwister kommen erfahrungsgemäß auf 0,3 bis 0,5. Mit gleicher Frisur und Brille steigt der Wert. |
| Schwelle verstellen | immer | Der ehrlichste Angriff: Die Sicherheit *ist* diese Zahl. |
| `data/faceid.npy` austauschen | immer | Wer die Referenzdatei ersetzen kann, braucht kein Gesicht. In echten Systemen liegt diese Datei deshalb in gesicherter Hardware – beim iPhone in der Secure Enclave, für die Software unerreichbar. |

**Die Auflösung:** Echtes Face ID projiziert rund 30 000 Infrarotpunkte auf das
Gesicht und misst deren Abstände. Es sieht also Tiefe. Ein Foto ist flach und
fällt durch. Diese Prüfung heißt **Liveness** – und die Klasse hat gerade selbst
bewiesen, warum es sie braucht.

---

## Antworten auf die Einstiegsfrage

Am Ende wird das Plakat von 8:05 durchgegangen. Diese Punkte sollten am Schluss
dort stehen:

1. Die Kamera hat **Helligkeitswerte** aufgenommen – eine Tabelle aus Zahlen.
2. Ein neuronales Netz hat daraus **128 Zahlen** berechnet.
3. Diese wurden mit **gespeicherten 128 Zahlen** verglichen.
4. Das Ergebnis war **ein einziger Ähnlichkeitswert**.
5. Dieser wurde mit einer **Schwelle** verglichen, die jemand festgelegt hat.
6. Zusätzlich prüft das Handy mit Infrarot, ob überhaupt ein **lebendes Gesicht**
   davor ist.

Häufige Vermutungen, die sich als Mythos erweisen: „Das Handy vergleicht das Foto
mit einem gespeicherten Foto" (nein, es speichert kein Bild), „es erkennt mich an
den Augen" (nein, an einem Gesamtmuster, das niemand einzeln benennen kann),
„das läuft über das Internet" (nein, es bleibt auf dem Gerät).

---

## Advanced-Stationen

Fünf eigenständige Programme für schnelle Gruppen. Sie brauchen alle die
Aufnahmen aus Station 4a und weisen freundlich darauf hin, wenn zu wenige da
sind.

### 91 · Der Gesichtsraum als Schatten

`uv run code/91_gesichtsraum.py`

Die Hauptkomponentenanalyse projiziert die 128-dimensionalen Vektoren auf eine
Ebene. **Was zu erwarten ist:** Aufnahmen derselben Person liegen als Gruppe
zusammen und sind durch eine Linie verbunden, verschiedene Personen liegen weit
auseinander. Oben rechts steht, wie viel Prozent der Streuung dieser Schatten
zeigt – bei acht bis zwanzig Aufnahmen typisch **50 bis 75 Prozent**.

Die wichtige Nachfrage: *Wenn zwei Punkte im Bild nebeneinander liegen – sind
sie dann dieselbe Person?* Nein. Sie können in den 126 nicht gezeichneten
Richtungen weit auseinander liegen. Der Schatten kann täuschen, die Rechnung mit
allen 128 Zahlen nicht.

Sind die Gruppen bei euch unrealistisch dicht beieinander, wurden beide
Aufnahmen im selben Moment gemacht. Mit unterschiedlichem Licht und Kopfdrehung
werden die Gruppen lockerer – und das Bild ehrlicher.

### 92 · Die Fehlerkurve

`uv run code/92_fehlerkurve.py`

Zeichnet FRR (rot, steigend) und FAR (cyan, fallend) über dem Schwellenwert, dazu
die Schwelle des Modells als grüne Linie und den Schnittpunkt als weißen Kreis.
Der Schnittpunkt heißt **Equal Error Rate**. Bei Klassendaten liegt er meist
zwischen **0,2 und 0,45**.

Kernaussage: Die eine Kurve steigt, wo die andere fällt. Es gibt keine Schwelle,
bei der beide null sind – man wählt nur, welchen Fehler man lieber macht.

### 93 · Das Durchschnittsgesicht

`uv run code/93_durchschnitt.py`

Vier Kacheln: Gesicht A, die Mischung, Gesicht B und der Mittelwert aller
Aufnahmen. Der Regler steuert `t` in `(1-t)·A + t·B`. Dass das überhaupt
funktioniert, liegt am `alignCrop` des Modells – alle Gesichter sind auf
112 × 112 Pixel gerade gedreht, Augen an derselben Stelle.

Anschlussfrage: Das Durchschnittsgesicht wirkt auf viele Menschen besonders
ebenmäßig. Schönheitsfilter rechnen genau in diese Richtung – wollen wir das?

### 94 · Das Kernel-Labor

`uv run code/94_kernel_labor.py`

Neun Regler von −8 bis +8, dazu Summe und Deutung live im Bild.

| Aufgabe im Kopf der Datei | Lösung |
|---|---|
| Nur senkrechte Kanten | `[[-1,0,1],[-2,0,2],[-1,0,1]]` – die Nullen stehen senkrecht |
| Nur waagerechte Kanten | dasselbe um 90 Grad gedreht: `[[-1,-2,-1],[0,0,0],[1,2,1]]` |
| Bild nach rechts verschieben | eine einzige `1` in der linken Spalte, sonst Nullen |
| Nichts passiert | nur die Mitte auf `1`, alles andere `0` (Summe 1) |
| Eine `1` außerhalb der Mitte | Das Bild wird verschoben – die Faltung schaut auf den Nachbarpixel und übernimmt dessen Wert |

Die Anzeige der Summe nimmt die Bonusfrage aus Station 2 auf: Summe 1 erhält die
Helligkeit, Summe 0 ergibt einen Kantenfilter, größer als 1 macht heller.

### 90 · Die Anwesenheitsliste

`uv run code/90_anwesenheit.py`

Mehrere Personen anmelden, Namen erscheinen live neben den Gesichtern. Technisch
nichts Neues – aber die Frage danach ist der Punkt: *Wollt ihr, dass so etwas im
Klassenzimmer hängt?* Das Programm ist eine Überwachungsanlage in rund 120 Zeilen
Python, und genau deshalb steht es am Ende.
