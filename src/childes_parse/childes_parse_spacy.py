"""Main module."""
import benepar
import spacy
import os
import nltk
from tqdm import tqdm

# Download benepar model
benepar.download('benepar_en3')

# Load spacy tokenizer
nlp = spacy.load('en_core_web_lg')

# Add benepar parser if not already added
if "benepar" not in nlp.pipe_names:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

# Function to parse a text file
def parse_text_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        text = infile.read().split("\n")

    parsed_sentences = []
    for line in tqdm(text, desc=f"Parsing {input_path}"):
        if line.strip():
            doc = nlp(line)
            parsed_sentences.extend(sent._.parse_string for sent in doc.sents)

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(parsed_sentences))

# Define input and output folders
input_folder =  "../../data/AOCHILDES"
output_folder = "../../data/PARSED"
os.makedirs(output_folder, exist_ok=True)

# Process each text file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(".txt", ".parsed"))
        parse_text_file(input_file, output_file)
