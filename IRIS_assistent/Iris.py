from sprache import sprache_erkennen
from sprecher import sprich
from ki_Iris import Iris_brain

def main():
    sprich("Halloich bin Iris.Wie kann ich ihnen helfen.")
    while True:
        text = sprache_erkennen()
        if not text:
            continue

        low = text.lower()
        if any(k in low for k in ("stopp", "exit", "beenden", "tschüss", "auf wiedersehen")):
            sprich("Na endlich. Ich dachte schon, du gehst nie.")
            break

        antwort = Iris_brain(text)
        sprich(antwort)

if __name__ == "__main__":
    main()