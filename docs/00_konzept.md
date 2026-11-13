# Face it! – Didaktisches Konzept

**Workshop zu Computer Vision am Beispiel der Gesichtserkennung**

| | |
|---|---|
| **Schule** | Städtisches Albert-Schweitzer-Gymnasium Plettenberg |
| **Zielgruppe** | Differenzierungskurse Mathematik, Klasse 10 |
| **Dauer** | 3 × 90 Minuten an drei Terminen, gegliedert in sechs Blöcke |
| **Programmiervorkenntnisse** | keine vorausgesetzt |
| **Gruppengröße** | bis 20 Schüler:innen in 8 festen Gruppen, 2–3 pro Rechner |

---

## 0. Einsatzkontext: ein Mathematik-Differenzierungskurs

Das ist keine beliebige zehnte Klasse. Diese Schüler:innen haben Mathematik im
Wahlpflichtbereich **selbst gewählt** – sie sind der Sache gegenüber offen und
halten es aus, wenn eine Erklärung zwei Schritte braucht. Programmieren können
sie trotzdem nicht, und darauf ist der Workshop ausgelegt.

Der Unterschied zeigt sich nicht im Tempo, sondern in der **Tiefe an drei
Stellen**: beim Vektorbegriff, beim Ähnlichkeitsmaß und bei den Fehlerraten. Wer
mag, kann dort weitergehen als in einer regulären Klasse – die folgende Tabelle
zeigt, wo der Workshop an bekannten Stoff anknüpft.

### Anknüpfung an den Mathematikunterricht

| Station | Mathematischer Kern | Anschluss |
|---|---|---|
| 1 · Pixel | Bild als **Matrix** über {0, …, 255} | Matrizen als Datenstruktur, nicht als Rechenschema. Auflösung 16 × 16 heißt: 256 Einträge. |
| 2 · Faltung | **Skalarprodukt** eines 3×3-Fensters mit dem Kernel, gleitend über die Matrix | Jedes Ergebnisfeld ist ein Skalarprodukt aus neun Produkten. Kernelsumme 0 → invariant gegenüber konstanter Verschiebung: der Filter „sieht" nur Änderung. |
| 4 · Embedding | Punkt im **ℝ¹²⁸** | Von ℝ² über ℝ³ nach ℝ¹²⁸ – der Begriff Dimension löst sich von der Anschauung. |
| 4b · Ähnlichkeit | **Kosinus-Ähnlichkeit** cos θ = (a·b)/(‖a‖·‖b‖) | Skalarprodukt und Norm aus dem Unterricht, hier als Ähnlichkeitsmaß. Warum nicht der euklidische Abstand? Weil der Winkel von der Vektorlänge unabhängig ist. |
| 5 · Fehlerraten | **Bedingte Häufigkeiten**, Prozentrechnung, konkurrierende Zielgrößen | Falschakzeptanz und Falschabweisung als Funktionen des Schwellenwerts – zwei Kurven, die sich gegenläufig verhalten. Wer will, skizziert sie. |
| 3b · Netz | **Delaunay-Triangulation** einer Punktmenge | Geometrie zum Anfassen: 68 Punkte, 114 Dreiecke, Kriterium der Umkreise. |
| Advanced 91 | **Hauptkomponentenanalyse** über die Singulärwertzerlegung | Der 128-dimensionale Raum wird auf eine Ebene projiziert. Die Klasse sieht ihre eigenen Punkte als Gruppen – und daneben steht, wie viel Prozent der Streuung dieser Schatten überhaupt zeigt. |
| Advanced 92 | Zwei gegenläufige **Fehlerfunktionen** und ihr Schnittpunkt | FAR und FRR als Kurven über dem Schwellenwert, mit der Equal Error Rate als Schnittpunkt. |
| Advanced 93 | **Konvexkombination** (1−t)·A + t·B | Verbindungsstrecke zwischen zwei Punkten – nur mit 37 632 Koordinaten gleichzeitig. |

Diese Anschlüsse sind **Angebote, kein Pflichtprogramm**. Der Workshop trägt
auch ohne sie – aber in einem Mathematikkurs wäre es verschenkt, das
Skalarprodukt nicht zu benennen, wenn die Klasse es gerade zwölfmal von Hand
ausgerechnet hat.

---

## 1. Leitidee

Die Schüler:innen entsperren jeden Tag ihr Handy mit dem Gesicht. Sie halten das für
Magie oder für "das Handy erkennt mich halt". Der Workshop zerlegt diese Alltagsmagie in
vier Schritte, die sie **selbst nachbauen** – und am Ende selbst **aushebeln**.

Der rote Faden ist eine einzige Frage, die am Anfang an der Tafel steht und am Ende
beantwortet wird:

> **Was genau hat mein Handy gerade getan, als es mein Gesicht erkannt hat?**

## 2. Die vier Aha-Momente

Jede Station hat genau **einen** Aha-Momente.

| # | Station | Aha-Moment | Belegt durch |
|---|---------|-----------|--------------|
| 1 | Bild = Tabelle | "Der Computer sieht kein Gesicht, er sieht Zahlen von 0 bis 255." | Eigenes Webcam-Foto als Zahlengitter im Terminal, danach auf Papier ausgemalt |
| 2 | Filter & Faltung | "Ich war gerade selbst ein neuronales Netz." | 3x3-Kernel per Hand auf Papier gerechnet, dann derselbe Kernel live auf der Webcam |
| 3 | Detektion ≠ Erkennung | "Erkennung ist Statistik, nicht Wahrheit." | Die Detektion findet Gesichter auf Postern, Zeichnungen und Fotos – und übersieht das echte |
| 4 | Gesicht = Punkt im Raum | "Ich bin für den Computer eine Liste aus 128 Zahlen – und Sicherheit ist ein Schwellenwert, den irgendwer gewählt hat." | Eigene Face-ID mit Schieberegler: bei 0,1 entsperrt jeder, bei 0,9 niemand |

Block 6 (**Angriff & Ethik**) ist kein fünfter Inhalt, sondern die
*Konsequenz* aus Station 3 und 4: Wenn Erkennung nur ein Zahlenvergleich mit
Schwellenwert ist, dann ist sie angreifbar und fehlerbehaftet. Und manche Fehler sind gefährlicher als andere.

## 3. Methodische Grundsätze

1. **Neun Folien im ganzen Workshop**, eine Fazit-Folie pro Block plus Titel, Ausblick
   und Take-home. Jeder Input dauert < 5 Minuten und steht
   *nach* dem Experiment, nicht davor. Erst staunen, dann erklären.
2. **Fachbegriffe kommen zuletzt.** Die SuS erleben erst das Phänomen, dann bekommt es
   einen Namen ("das, was du gerade gebaut hast, heißt Faltung / Embedding /
   False-Accept-Rate").
3. **Kein Code von Null.** Bei Nullvorkenntnissen scheitert freies Programmieren am
   Semikolon, nicht am Konzept. Stattdessen: fertige Skripte, in denen die SuS
   * Zahlen in einer Liste ändern (Kernel),
   * eine kommentierte Zeile aktivieren (`# img = 255 - img`),
   * einen Wert an einem Schieberegler verstellen (Schwellenwert),
   * genau eine Zeile selbst schreiben (die Vergleichszeile in Station 4).
4. **Jedes Skript läuft in < 3 Sekunden und zeigt sofort ein Bild.** Kein Warten, kein
   Training, keine GPU, kein Internet.
5. **Zwei bis drei SuS pro Rechner, in festen Gruppen.** Eine Person tippt, eine sitzt
   vor der Kamera – Rollentausch pro Station. Gesichtserkennung braucht zwingend ein
   zweites Gesicht, ein drittes schadet nicht. Gruppe und Rechner bleiben über alle drei
   Termine gleich.
6. **Unplugged-Anteil.** Station 2 beginnt auf Papier. Wer Faltung einmal mit dem
   Bleistift gerechnet hat, vergisst sie nicht.
7. **Wettbewerb statt Arbeitsblatt.** "Experimente-Bingo" (Station 3) und
   "Hack-Challenge" (Block 6) erzeugen Ehrgeiz und produzieren dabei genau die
   Fehlerfälle, über die wir reden wollen.
8. **Hausaufgaben, die tragen.** Zwischen den Terminen liegen jeweils eine Woche oder
   mehr. Jede Hausaufgabe funktioniert ohne Rechner und wird im nächsten Termin wirklich
   gebraucht: die ausgemalten Blätter eröffnen Termin 2, das Angriffsmaterial macht die
   Hack-Challenge erst möglich, der vorbereitete Satz trägt die Diskussion in Block 6.
   Wer sie weglässt, merkt es selbst. Die Liste steht in
   [01_agenda.md](01_agenda.md#hausaufgaben).

## 4. Lernziele

Die Schüler:innen können am Ende ...

**Fachlich**
- ein digitales Bild als Matrix von Helligkeitswerten beschreiben (Pixel, Graustufe, Auflösung);
- die Wirkung eines Filterkernels erklären und einen Kantenfilter von einer Weichzeichnung unterscheiden;
- zwischen *Gesichtsdetektion* (Wo ist ein Gesicht?) und *Gesichtserkennung* (Wessen Gesicht?) unterscheiden;
- erklären, dass Gesichtserkennung ein Bild in einen Zahlenvektor übersetzt und Ähnlichkeit als Abstand misst;
- beschreiben, wie ein Schwellenwert zwischen Falschakzeptanz und Falschabweisung abwägt.

**Überfachlich / ethisch**
- mindestens drei Angriffswege auf ein Gesichtserkennungssystem benennen und erklären, warum echtes Face-ID eine Tiefenkamera braucht;
- begründen, warum biometrische Daten rechtlich besonders geschützt sind (DSGVO Art. 9) und was der EU AI Act für Echtzeit-Gesichtserkennung im öffentlichen Raum vorsieht;
- eine eigene Position zu einem Anwendungsfall (Bahnhof, Schule, Handy) formulieren und mit einem technischen Argument stützen.

## 5. Technische Entscheidung und ihre Begründung

**Stack: Python + `opencv-python` + `numpy`. Nichts weiter.**

| Anforderung | Umsetzung |
|---|---|
| Gesichtsdetektion klassisch | Haar-Cascade, in OpenCV enthalten (`cv2.data.haarcascades`) |
| Landmarks (optional, Station 3b) | **LBF** (`cv2.face`), 68 Punkte, daraus ein Delaunay-Netz |
| Gesichtsdetektion modern | **YuNet** (`cv2.FaceDetectorYN`), ONNX-Datei ~340 KB, liegt im Repo |
| Gesichts-Embedding (128 Zahlen) | **SFace** (`cv2.FaceRecognizerSF`), ONNX-Datei ~37 MB, liegt im Repo |
| Ähnlichkeit | Kosinus-Ähnlichkeit, von OpenCV mitgeliefert; Standardschwelle 0,363 |

Warum nicht `face_recognition` / dlib? Das braucht auf Windows einen C++-Compiler und
scheitert in Schulnetzen regelmäßig. Warum nicht Colab? Weil Webcam-Zugriff dort über
JavaScript-Krücken läuft und WLAN in Klassenstärke der häufigste Grund für einen
gescheiterten Workshop ist. Die gewählte Variante ist **komplett offlinefähig** und mit
einem einzigen Befehl installiert: `uv sync`.

Für die optionale Station 3b (das Dreiecksnetz aus dem Workshop-Logo) kommt ein
Landmark-Modell hinzu – schön, aber nicht tragend, und nur auf dem zentralen Rechner am
Beamer nötig.

## 6. Datenschutz im Workshop selbst

Der Workshop erhebt biometrische Daten von Minderjährigen. Das wird nicht nebenbei
gemacht, sondern zum Lerninhalt:

- Alle Aufnahmen bleiben **lokal** im Ordner `data/` auf dem jeweiligen Rechner. Kein
  Upload, keine Cloud, kein Netzwerk.
- Vorab: Einwilligung der Eltern (Vorlage: `material/elternbrief_und_einwilligung.html`).
- Wer nicht fotografiert werden möchte, arbeitet mit den bereitgestellten
  **frei lizenzierten** Portraits in `data/beispiele/` – **ohne Nachfrage und ohne
  Begründung**. (Die Lizenzen sind gemischt: teils Public Domain, überwiegend CC BY
  bzw. CC BY-SA; Urheber und Lizenz je Bild in `data/beispiele/CREDITS.md`.)
- **Gemeinsames Löschen als Schlussritual:** Am Ende führen alle gleichzeitig
  `99_cleanup.py` aus. Datensparsamkeit wird vorgeführt. Das passiert am Ende **jedes
  der drei Termine**, nicht nur am Schluss – sonst lägen Gesichtsvektoren wochenlang
  auf Schulrechnern.
- **Die eigenen Vergleichsbilder folgen derselben Regel wie die Lerninhalte.** In
  `data/personen/` liegen Portraits für die Beamer-Demo in Station 4b – ausschließlich
  **verstorbene** Personen und ausschließlich **Public Domain**. Begründung: Ein
  Gesichtsvektor ist biometrische Verarbeitung nach Art. 9 DSGVO, und eine Lizenz deckt
  nur das Urheberrecht, nicht Persönlichkeitsrecht und Datenschutz. Ein Workshop, der
  Clearview AI für genau diese Verarbeitung kritisiert, kann sie nicht selbst an
  lebenden Personen vornehmen. Das postmortale Persönlichkeitsrecht besteht fort; die
  Nutzung bekannter zeitgeschichtlicher Bildnisse im Unterricht ist davon nach
  hiesiger Einschätzung gedeckt – bei Veröffentlichung über den Kurs hinaus gehört die
  Frage zur Datenschutzbeauftragten der Schule.

## 7. Differenzierung

- **Advanced-Stationen** für schnelle Gruppen: fünf eigenständige Programme
  (`90` bis `94` im Startmenü), die den Stoff mathematisch weiterdrehen –
  Hauptkomponentenanalyse, Fehlerkurven, Gesichtsmittelwerte, freies Kernel-Labor,
  Anwesenheitsliste. Sie sind auch das Take-home-Material.
- **Advanced-Blöcke im Code**: In `01_pixel.py` steht ein Abschnitt mit
  auskommentierten Zeilen (Negativ, Posterisierung, Schwellenwert). Wer das
  `#` entfernt, sieht die Wirkung sofort im laufenden Bild.
- **Rettungsanker**: Alle Antworten, Kernel-Lösungen und erwarteten Zahlenwerte
  stehen in [docs/03_loesungen.md](03_loesungen.md). Wer feststeckt, bekommt einen
  Hinweis statt zu warten.
- **Fehlerkarte**: Die drei häufigsten Fehler stehen unten auf dem Laufzettel, zehn
  weitere auf der Innenseite der Ampelkarte – das spart der Lehrkraft rund 20 Minuten
  Supportlaufen.
- **Ampelkarte** (`material/handouts/handout_E_ampelkarte.html`): eine gefaltete
  A5-Karte, grün auf der einen und rot auf der anderen Seite. Jede Gruppe stellt sie
  auf: grün heißt „Station geschafft", rot heißt „wir kommen nicht weiter". Die
  Lehrkraft sieht den Stand der ganzen Gruppe mit einem Blick über den Raum, ohne
  zu fragen – und niemand muss die Hand heben. Auf der Innenseite steht die
  Fehlerhilfe, verbunden mit der Regel: erst lesen, dann Nachbargruppe, dann rot.
