from typing import Set, List, Optional, Tuple
from pathlib import Path
import os
import pandas as pd
import re
import argparse
from dictionaries import w2string
import string

# Get the root folder (two levels up)
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the path to the 'data' folder
data_folder = os.path.join(root_folder, "data/CHILDES")
output_folder = os.path.join(root_folder, "data/AOCHILDES")

print("Data Folder Path:", data_folder)


ignore_regex = re.compile(r'(�|www|xxx|yyy)')



"""Filtering Functions"""
def extract_age_from_file(file_path: Path) -> Optional[int]:
    """Extract child's age (in months) from the @ID line in a CHILDES .cha file."""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@ID:") and "Target_Child" in line or "Child" in line:
                # Updated regex to handle different spacing and field variations
                match = re.search(r'eng\|[^|]*\|[^|]*\|(\d+);(\d*)', line)                
                if match:
                    years = int(match.group(1))
                    # Handle missing or empty months
                    months_str = match.group(2)
                    months = int(months_str) if months_str and months_str.isdigit() else 0
                    return years * 12 + months  # Convert to months
                
    return None  # If no age is found

def find_cha_files(data_folder: Path, min_age: int = 0, max_age: int = 12) -> List:
    """Recursively find all .cha files and filter by child age."""
    selected_files = []

    for dirpath, _, filenames in os.walk(data_folder):
        for file in filenames:
            if file.endswith(".cha"):
                file_path = os.path.join(dirpath, file)

                # Extract child's age
                child_age_months = extract_age_from_file(file_path)
                # Check if age falls within range
                if child_age_months is not None and min_age <= child_age_months < max_age:
                    selected_files.append(file_path)

    return selected_files

def extract_child_speakers(file_path: Path) -> set():
    child_speakers = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@ID"):
                parts = line.split("|")
                if "Target_Child" in parts or "Child" in parts:
                    speaker_code = parts[2]
                    child_speakers.add(f"*{speaker_code}:")
    return child_speakers

""" Cleaning Functions"""

def clean_line(line):
    """Normalize text by removing punctuation, fixing spelling, and splitting compounds."""
    line = re.sub(r'\d+_\d+', '', line)  # Remove timestamps
    line = re.sub(r'^\*\w+:\s*', '', line)  # Remove speaker labels (*MOT:, *FAT:)

    # Ignore lines matching the regex (e.g., unwanted characters, website links)
    if ignore_regex.search(line):
        return None

    # Lowercase the entire utterance
    line = line.lower()

    # Remove bracketed annotations (e.g., [=! silence], [/], [=! laughs])
    line = re.sub(r'<[^>]+>', '', line)  # Remove angled brackets <you>
    line = re.sub(r'(?:\b\d+ )?\[.*?\]|\(.*?\)|\{.*?\}|\&=[^\s]+', '', line)  # Remove bracket content 0 [=! laughs]

    # Remove @ annotations
    line = re.sub(r'\b\w+@\w+\b', '', line)

    # Remove (3.), (5.), etc.
    line = re.sub(r'\(\d+\.\)', '', line)

    # Fix spelling errors using predefined dictionary
    words = line.split()
    words = [w2string.get(word, word) for word in words]

    # Split compound words (replace + and _ but keep hyphens)
    line = " ".join(words).replace('+', ' ').replace('_', ' ')

    # Remove all punctuation except hyphens
    # line = line.translate(str.maketrans('', '', string.punctuation.replace('-', '')))

    # Remove repeated words (e.g., "tickle tickle tickle" → "tickle")
    line = re.sub(r'\b(\w+)( \1\b)+', r'\1', line)
    
    # Remove repeated syllables with hyphens (e.g., "-uh -uh -uh" → "-uh")
    line = re.sub(r'(-\w+)( \1)+', r'\1', line)

    # Remove ampersands
    line = re.sub(r'&', '', line)

    # Remove double space
    line = re.sub(r'\s{2,}', ' ', line)

    # Remove one-token utterances
    if len(line.split()) < 2:
        return None

    return line.strip()

def process_chat_files(file_path: Path, collected_lines):
    child_speakers = extract_child_speakers(file_path)
    recording = False

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("@Begin"):
                recording = True
                continue
            if not recording or line.startswith(("@", "%")):
                continue
            if any(line.startswith(child_speaker) for child_speaker in child_speakers):
                continue
            cleaned_line = clean_line(line)

            if cleaned_line:  # Avoid saving empty lines
                collected_lines.append(cleaned_line)

    print(f"Processed: {file_path}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Filter CHILDES .cha files based on child age.")
    parser.add_argument("min_age", type=int, help="Minimum child age in months")
    parser.add_argument("max_age", type=int, help="Maximum child age in months")

    # Parse arguments
    args = parser.parse_args()

    # Run file filtering
    filtered_files = find_cha_files(data_folder, args.min_age, args.max_age)

    print(f"Found {len(filtered_files)} files for age range {args.min_age}-{args.max_age} months.")
    #Run the cleaning and processing

    collected_lines = []

    for file_path in filtered_files:  # `filtered_files` comes from the age filtering step
        process_chat_files(file_path, collected_lines)

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"age_{args.min_age}_{args.max_age}.txt")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(collected_lines))
    
    print(f"processed data saved to {output_file}")