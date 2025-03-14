import re

def find_unusual_symbols(text):
    return re.findall(r'[^\w\s,.!?\'"-]', text)  # Captures non-standard symbols

with open("/home/argy/childes_parse/data/AOCHILDES/age_36_48.txt", "r", encoding="utf-8") as file:
    corpus_text = file.read()

symbols = set(find_unusual_symbols(corpus_text))
print("Unusual symbols found:", symbols)