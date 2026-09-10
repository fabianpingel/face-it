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

**Kernel-Challenge**

| Aufgabe | Lösung |
|---|---|
| Nur senkrechte Kanten | `[[-1,0,1],[-2,0,2],[-1,0,1]]` – Sobel in x-Richtung, Taste `5`. Merkregel: Die Nullen stehen **senkrecht** in der Mitte, also findet der Kernel senkrechte Kanten. |
| Nur waagerechte Kanten | Derselbe Kernel um 90 Grad gedreht: `[[-1,-2,-1],[0,0,0],[1,2,1]]`, Taste `6`. |
| Summe der neun Zahlen ungleich 1 | Ist die Summe **größer** als 1, wird das ganze Bild heller; ist sie **kleiner**, wird es dunkler. Bei Summe **0** bleibt nur die Veränderung übrig – das ist ein Kantenfilter. |
| 5 × 5-Weichzeichner | Zeichnet stärker weich als 3 × 3, weil über mehr Nachbarpixel gemittelt wird. Feine Strukturen wie Wimpern verschwinden zuerst. |

**Häufiger Stolperstein:** Ein Kernel, dessen Zahlen sich zu einer großen Summe
addieren, liefert ein fast weißes Bild. Das ist kein Fehler, sondern die Antwort
auf die Frage oben.

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

`uv run code/08_bias.py` braucht mindestens vier gespeicherte Aufnahmen und
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
