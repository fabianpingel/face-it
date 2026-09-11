"""
Test 5: Liefert die Webcam ein Bild?

Dieser Test ist der einzige, der echte Hardware braucht. Auf einem Rechner
ohne Kamera wird er uebersprungen, nicht als Fehler gemeldet - der Workshop
laeuft im Notfall auch mit FACEIT_KAMERA und einem gespeicherten Bild.

Die Kamera wird hier absichtlich direkt geoeffnet und nicht ueber
faceit.kamera_oeffnen(): das beendet bei einem Fehlschlag das ganze Programm
mit einer Hilfemeldung, was fuer einen Test das falsche Verhalten ist.
"""

import os

import pytest

# Erster Test in dieser Datei, der Hardware anfasst: Das Ersatzbild muss weg,
# sonst wuerde es die echte Kamera verdecken.
ERSATZ = os.environ.pop("FACEIT_KAMERA", None)


def kamera_oeffnen_ohne_abbruch(index=0):
    """Versucht die Kamera zu oeffnen. Gibt None zurueck, wenn es nicht geht."""
    import cv2

    backends = [cv2.CAP_DSHOW, cv2.CAP_ANY] if os.name == "nt" else [cv2.CAP_ANY]
    for backend in backends:
        kamera = cv2.VideoCapture(index, backend)
        if kamera.isOpened():
            return kamera
        kamera.release()
    return None


@pytest.fixture(scope="module")
def kamera():
    geraet = kamera_oeffnen_ohne_abbruch()
    if geraet is None:
        pytest.skip(
            "Keine Webcam ansprechbar. Moegliche Gruende:\n"
            "  1) Ein anderes Programm belegt sie (Teams, Zoom, Kamera-App)\n"
            "  2) Windows blockiert den Zugriff: Einstellungen > Datenschutz "
            "und Sicherheit > Kamera > 'Apps den Zugriff erlauben' UND "
            "'Desktop-Apps den Zugriff erlauben'\n"
            "  3) Der Rechner hat keine Kamera - dann im Notfall-Modus "
            "arbeiten:\n"
            "     set FACEIT_KAMERA=data/beispiele/portrait_01.jpg"
        )
    yield geraet
    geraet.release()


def test_kamera_liefert_ein_bild(kamera):
    erfolg, bild = kamera.read()
    assert erfolg and bild is not None, (
        "Die Kamera ist offen, liefert aber kein Bild. Das passiert, wenn ein "
        "anderes Programm sie gleichzeitig benutzt."
    )


def test_bild_hat_sinnvolle_groesse(kamera):
    _, bild = kamera.read()
    hoehe, breite = bild.shape[:2]
    assert breite >= 320 and hoehe >= 240, (
        f"Das Kamerabild ist nur {breite} x {hoehe} Pixel gross. Damit findet "
        "die Gesichtserkennung in Station 3 nichts."
    )


def test_bild_ist_farbig(kamera):
    """Station 1 rechnet mit drei Farbkanaelen (R, G, B)."""
    _, bild = kamera.read()
    assert bild.ndim == 3 and bild.shape[2] == 3, (
        f"Das Kamerabild hat die Form {bild.shape} statt (Hoehe, Breite, 3)."
    )


def test_bild_ist_nicht_schwarz(kamera):
    """
    Eine abgeklebte oder von Windows stillgelegte Kamera liefert manchmal
    lauter Nullen statt eines Fehlers. Das faellt sonst niemandem auf.
    """
    # Ein paar Bilder verwerfen: manche Kameras brauchen einen Moment,
    # bis die Belichtung sitzt.
    for _ in range(5):
        kamera.read()
    _, bild = kamera.read()

    assert bild.max() > 10, (
        "Das Kamerabild ist vollstaendig schwarz. Ist die Linse abgeklebt oder "
        "der Sichtschutz zu?"
    )


def test_windows_kamerafreigabe():
    """
    Prueft die Windows-Datenschutzeinstellung. Sie kann auf 'Deny' stehen,
    obwohl eine Kamera vorhanden ist - dann schlaegt der Zugriff ohne
    Fehlermeldung fehl, was der haeufigste Stolperstein ist.
    Nur eine Meldung, kein Fehler: manche Systeme fuehren den Schluessel nicht.
    """
    if os.name != "nt":
        pytest.skip("Nur unter Windows relevant.")

    import winreg

    pfad = (r"Software\Microsoft\Windows\CurrentVersion"
            r"\CapabilityAccessManager\ConsentStore\webcam")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, pfad) as schluessel:
            wert, _ = winreg.QueryValueEx(schluessel, "Value")
    except OSError:
        pytest.skip("Der Kamera-Freigabeschluessel ist auf diesem System nicht "
                    "gesetzt - das ist normal und kein Fehler.")

    assert wert != "Deny", (
        "Windows verweigert Apps den Kamerazugriff. Zu aendern unter:\n"
        "  Einstellungen > Datenschutz und Sicherheit > Kamera\n"
        "  'Apps den Zugriff auf die Kamera erlauben' einschalten,\n"
        "  ebenso 'Desktop-Apps den Zugriff erlauben'."
    )
