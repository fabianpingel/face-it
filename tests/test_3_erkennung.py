"""
Test 3: Funktioniert die Fachlogik?

Das ist der wichtigste Test: er geht die ganze Kette aus Station 2 bis 4
durch - Faltung, Gesicht finden, 128 Zahlen berechnen, Aehnlichkeit messen -
und zwar auf den beigelegten Portraits, ohne Kamera.

Wenn dieser Test gruen ist, funktioniert der Workshop inhaltlich.
"""

import numpy as np
import pytest

from conftest import zahlen_aus_portrait


# ----------------------------------------------------------- Station 2: Faltung

SOBEL = np.array([[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]])


def falten(bild, kernel):
    """Dieselbe Rechnung, die die Klasse auf Arbeitsblatt B von Hand macht."""
    hoehe, breite = bild.shape
    k = kernel.shape[0] // 2
    ergebnis = np.zeros((hoehe - 2 * k, breite - 2 * k), dtype=int)
    for z in range(ergebnis.shape[0]):
        for s in range(ergebnis.shape[1]):
            fenster = bild[z:z + kernel.shape[0], s:s + kernel.shape[1]]
            ergebnis[z, s] = int((fenster * kernel).sum())
    return ergebnis


def test_kernel_summe_ist_null():
    """
    Die Begruendung auf Folie 3: Der Filter reagiert nicht auf Helligkeit,
    weil sich seine neun Zahlen zu null addieren.
    """
    assert SOBEL.sum() == 0


def test_gleichmaessige_flaeche_ergibt_null():
    """Folie 3, linke Zahl: in der Flaeche steht 0 - egal wie hell sie ist."""
    for helligkeit in (0, 3, 7, 9, 255):
        flaeche = np.full((5, 5), helligkeit)
        assert (falten(flaeche, SOBEL) == 0).all(), (
            f"Bei gleichmaessiger Helligkeit {helligkeit} kam nicht 0 heraus."
        )


def test_kante_ergibt_nicht_null():
    """Folie 3, rechte Zahl: auf der Kante steht ein Wert deutlich ueber 0."""
    bild = np.zeros((5, 5), dtype=int)
    bild[:, 3:] = 9                      # senkrechte Kante zwischen Spalte 2 und 3
    ergebnis = falten(bild, SOBEL)
    assert abs(ergebnis).max() > 0, "Die Kante wurde nicht gefunden."
    # Vier mal 9 auf der rechten Kernelhaelfte, Gewichte 1 + 2 + 1 = 4
    assert abs(ergebnis).max() == 4 * 9


def test_filter_ist_richtungsabhaengig():
    """
    Die Entdeckung aus Station 2: derselbe Kernel findet die senkrechte Kante
    und bleibt bei der waagerechten blind.
    """
    senkrecht = np.zeros((5, 5), dtype=int)
    senkrecht[:, 3:] = 9
    waagerecht = senkrecht.T

    assert abs(falten(senkrecht, SOBEL)).max() > 0
    assert abs(falten(waagerecht, SOBEL)).max() == 0, (
        "Der senkrechte Sobel-Kernel darf die waagerechte Kante nicht finden."
    )


# ----------------------------------------------- Station 3: Gesichter finden

def test_gesicht_wird_in_portraits_gefunden(fc, detektor, portraits):
    """YuNet muss in den beigelegten Portraits Gesichter finden."""
    import cv2

    gefunden = 0
    for pfad in portraits:
        bild = cv2.imread(str(pfad))
        assert bild is not None, f"Bild laesst sich nicht laden: {pfad}"
        if fc.gesichter_finden(detektor, bild):
            gefunden += 1

    assert gefunden >= 2, (
        f"Nur in {gefunden} von {len(portraits)} Portraits wurde ein Gesicht "
        "gefunden. Erwartet werden mindestens zwei - sonst laufen Station 4b "
        "und 5 nicht."
    )


def test_gesichtsrahmen_hat_vier_werte(fc, detektor, portraits):
    """Ein Fund ist ein Rechteck: x, y, Breite, Hoehe."""
    import cv2

    for pfad in portraits:
        bild = cv2.imread(str(pfad))
        gesichter = fc.gesichter_finden(detektor, bild)
        if not gesichter:
            continue
        x, y, breite, hoehe = gesichter[0][:4]
        assert breite > 0 and hoehe > 0
        assert 0 <= x < bild.shape[1] and 0 <= y < bild.shape[0]
        return
    pytest.skip("Kein Gesicht gefunden - siehe vorheriger Test")


# ------------------------------------- Station 4: 128 Zahlen und Aehnlichkeit

def test_embedding_hat_128_zahlen(fc, detektor, erkenner, portraits):
    """Der Kernsatz von Station 4a: dein Gesicht ist eine Liste aus 128 Zahlen."""
    for pfad in portraits:
        zahlen = zahlen_aus_portrait(fc, detektor, erkenner, pfad)
        if zahlen is None:
            continue
        assert zahlen.size == 128, (
            f"Das Modell liefert {zahlen.size} Zahlen statt 128."
        )
        return
    pytest.skip("Kein Gesicht in den Portraits gefunden")


def test_gleiches_bild_ist_sich_selbst_aehnlich(fc, detektor, erkenner, portraits):
    """Ein Gesicht mit sich selbst verglichen muss nahe 1,0 liegen."""
    for pfad in portraits:
        zahlen = zahlen_aus_portrait(fc, detektor, erkenner, pfad)
        if zahlen is None:
            continue
        wert = fc.aehnlichkeit(zahlen, zahlen)
        assert wert > 0.99, (
            f"{pfad.name} mit sich selbst ergibt nur {wert:.3f} statt fast 1,0."
        )
        return
    pytest.skip("Kein Gesicht in den Portraits gefunden")


def test_verschiedene_personen_liegen_unter_der_schwelle(
        fc, detektor, erkenner, portraits):
    """
    Der Kern von Station 4c: verschiedene Personen bleiben unter dem
    Schwellenwert. Sonst wuerde die Face ID jeden entsperren.
    """
    zahlen = []
    for pfad in portraits:
        z = zahlen_aus_portrait(fc, detektor, erkenner, pfad)
        if z is not None:
            zahlen.append((pfad.name, z))
    if len(zahlen) < 2:
        pytest.skip("Weniger als zwei verwertbare Portraits")

    hoechster = 0.0
    paar = ("", "")
    for i in range(len(zahlen)):
        for j in range(i + 1, len(zahlen)):
            wert = fc.aehnlichkeit(zahlen[i][1], zahlen[j][1])
            if wert > hoechster:
                hoechster, paar = wert, (zahlen[i][0], zahlen[j][0])

    assert hoechster < fc.SCHWELLE, (
        f"{paar[0]} und {paar[1]} erreichen {hoechster:.3f} und liegen damit "
        f"ueber dem Schwellenwert {fc.SCHWELLE}. Das sind verschiedene "
        "Personen - die Erkennung arbeitet nicht richtig."
    )


def test_aehnlichkeit_ist_symmetrisch(fc, detektor, erkenner, portraits):
    """cos(a,b) muss dasselbe sein wie cos(b,a) - sonst waere es kein Abstand."""
    zahlen = []
    for pfad in portraits:
        z = zahlen_aus_portrait(fc, detektor, erkenner, pfad)
        if z is not None:
            zahlen.append(z)
        if len(zahlen) == 2:
            break
    if len(zahlen) < 2:
        pytest.skip("Weniger als zwei verwertbare Portraits")

    hin = fc.aehnlichkeit(zahlen[0], zahlen[1])
    her = fc.aehnlichkeit(zahlen[1], zahlen[0])
    assert hin == pytest.approx(her, abs=1e-6)
