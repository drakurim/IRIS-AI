from datetime import datetime
import re
import difflib
import os_control

def _normalize(txt: str) -> str:
    t = txt.lower()
    t = (t.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
           .replace("ß", "ss"))
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t

def _fuzzy_contains(text: str, variants: list[str], threshold: float = 0.78) -> bool:
    words = text.split()
    for v in variants:
        if v in text:
            return True
    tokens = words + [" ".join(pair) for pair in zip(words, words[1:])]
    for v in variants:
        for tok in tokens:
            if difflib.SequenceMatcher(None, tok, v).ratio() >= threshold:
                return True
    return False

def _extract_int(text: str) -> int | None:
    m = re.search(r"\b(\d{1,3})\b", text)
    if not m: return None
    try:
        val = int(m.group(1))
        return max(0, min(100, val))
    except:
        return None

def Iris_brain(nachricht: str) -> str:
    raw = nachricht or ""
    s = _normalize(raw)

    # --- Lautstärke ---
    if _fuzzy_contains(s, ["mute", "stumm", "stummschalten", "lautlos"]):
        ok = os_control.volume_mute(True)
        return "Stumm. Herrlich." if ok else "es scheint ein fehler gegeben zu haben."

    if _fuzzy_contains(s, ["lautstaerke", "volume", "sound"]):
        val = _extract_int(s)
        if val is not None:
            ok = os_control.volume_set(val)
            return f"Lautstärke auf {val} Prozent." if ok else "Deine Lautstärke ist so widerspenstig wie du."
        if "leiser" in s:  return "Benutze 'Lautstärke 30' wie ein erwachsener Mensch."
        if "lauter" in s:  return "Sag mir eine Zahl. Ich bin keine Hellseherin."

    # --- Power / Session ---
    if _fuzzy_contains(s, ["sperre", "sperren", "sperr", "bildschirm sperren", "lock", "pc sperren", "computer sperren", "sperrer"]):
        os_control.lock()
        return "Wirt geperrt."

    if _fuzzy_contains(s, ["herunterfahren", "shutdown", "fahr den pc runter", "pc runterfahren", "runterfahren", "ausschalten", "power off"]):
        os_control.shutdown()
        return "Wirt heruntergefahren."

    if _fuzzy_contains(s, ["neustart", "neu starten", "restart", "boot neu", "starte neu", "reboot"]):
        os_control.restart()
        return "Wirt neugestarted."

    if _fuzzy_contains(s, ["schlaf", "sleep", "standby", "ruhezustand"]):
        os_control.sleep()
        return "Gute Nacht. Nutz die Pause. Du brauchst sie."

    # --- Apps öffnen ---
    if _fuzzy_contains(s, ["oeffne", "offne", "oeffnen", "offnen", "starte", "starten", "mach auf"]):
        m = re.search(r"(oeffne|offne|oeffnen|offnen|starte|starten|mach auf)\s+(.+)", s)
        if m:
            ziel = m.group(2).strip().strip('"')
            ok = os_control.open_app(ziel)
            return f"Öffne {ziel}. Versuch’s, solange es dauert." if ok else f"Ich habe es versucht. Vielleicht existiert {ziel} nicht."

    # --- Infos ---
    if _fuzzy_contains(s, ["zeit", "uhr"]):
        return f"Es ist {datetime.now().strftime('%H:%M')} Uhr.."

    if _fuzzy_contains(s, ["wer bist du", "glados", "wie heisst du", "wie heißt du"]):
        return "Ich bin Iris. Dein Zilan OS ki assistent. Ein perfekt optimiertes System."

    if _fuzzy_contains(s, ["hilfe", "was kannst du", "befehle", "kommandos"]):
        return ("Sage: 'öffne chrome', 'herunterfahren', 'neustart', 'sperren', "
                "'lautstärke 30', 'mute'. Oder sag irgendwas Belangloses.")

    return "ICH habe nicht verstanden."

def antwort_generieren(nachricht: str) -> str:
    return Iris_brain(nachricht)