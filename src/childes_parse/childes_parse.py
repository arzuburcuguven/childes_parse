"""Main module."""
import benepar
import os
from tqdm import tqdm
from transformers import AutoTokenizer

benepar.download('benepar_en3_large')

#load BERT tokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

#Load benepar parser

benepar_parser =benepar.Parser('benepar_en3_large')

#Function to tokenize a sentence using BERT

def bert_tokenize(sentence):
    tokens = tokenizer.tokenize(sentence)
    return tokens

def parse_text_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        text = infile.read().split("\n")
    
    parsed_sentences =[]
    for line in tqdm(text,  desc=f"Parsing {input_path}"):
        if line.strip():
            tokens = bert_tokenize(line)
            tree = benepar_parser.parse(tokens)
            parsed_sentences.append(str(tree))

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(parsed_sentences))

input_folder =  "../../data/AOCHILDES"
output_folder = "../../data/PARSED"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(".txt", ".parsed"))
        parse_text_file(input_file, output_file)