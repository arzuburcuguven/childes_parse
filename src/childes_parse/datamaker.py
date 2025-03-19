from typing import List, Optional, Dict
from pathlib import Path
import os
import pandas as pd
import re
import argparse
from collections import defaultdict
from dictionaries import w2string
import string

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_folder = os.path.join(root_folder, "data/CHILDES")
output_folder = os.path.join(root_folder, "data/AOCHILDES")

ignore_regex = re.compile(r'(�|www|xxx|yyy)')

# Track metadata: files per age group and activity type counts
metadata = defaultdict(lambda: {"file_count": 0, "activities": defaultdict(int), "sentences": defaultdict(int)})


""" Filtering Functions """
def extract_age_from_file(file_path: Path) -> Optional[int]:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@ID:") and ("Target_Child" in line or "Child" in line):
                match = re.search(r'eng\|[^|]*\|[^|]*\|(\d+);(\d*)', line)                
                if match:
                    years = int(match.group(1))
                    months_str = match.group(2)
                    months = int(months_str) if months_str and months_str.isdigit() else 0
                    return years * 12 + months  
    return None  

def extract_activity_types(file_path: Path) -> List[str]:
    """Extract activity types from the @Types line in a CHILDES .cha file."""
    activities = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@Types:"):
                activities = line.strip().split(":")[1].strip().split(", ")
                break
    return activities


def find_cha_files(data_folder: Path, min_age: int, max_age: int) -> List:
    """Recursively find .cha files and filter by child age."""
    selected_files = []

    for dirpath, _, filenames in os.walk(data_folder):
        for file in filenames:
            if file.endswith(".cha"):
                file_path = os.path.join(dirpath, file)
                child_age_months = extract_age_from_file(file_path)

                if child_age_months is not None and min_age <= child_age_months < max_age:
                    selected_files.append(file_path)

                    # Update metadata for the age group
                    metadata[child_age_months]["file_count"] += 1
                    activities = extract_activity_types(file_path)
                    for act in activities:
                        metadata[child_age_months]["activities"][act] += 1

    return selected_files


""" Cleaning & Processing Functions """
def clean_line(line: str) -> Optional[str]:
    """Normalize text by removing punctuation, fixing spelling, and splitting compounds."""
    line = re.sub(r'\d+_\d+', '', line)  # Remove timestamps
    line = re.sub(r'^\*\w+:\s*', '', line)  # Remove speaker labels (*MOT:, *FAT:)

    if ignore_regex.search(line):
        return None

    line = line.lower()
    line = re.sub(r'<[^>]+>', '', line)  # Remove <you>
    line = re.sub(r'(?:\b\d+ )?\[.*?\]|\(.*?\)|\{.*?\}|\&=[^\s]+', '', line)  # Remove annotations
    line = re.sub(r'\b\w+@\w+\b', '', line)  # Remove @ annotations
    line = re.sub(r'\(\d+\.\)', '', line)  # Remove (3.), (5.), etc.
    line = re.sub(r'[\x15‡↫→@↑^]', '', line)
    line = re.sub(r'\b(O|mhm)\s*\.\s*', '', line)

    words = line.split()
    words = [w2string.get(word, word) for word in words]

    line = " ".join(words).replace('+', ' ').replace('_', ' ')
    line = re.sub(r'&', '', line)
    line = re.sub(r'\s{2,}', ' ', line)

    if len(line.split()) < 2:
        return None

    return line.strip()


def process_chat_files(file_path: Path, collected_lines: List[str], age_group: int):
    child_speakers = set()
    activities = extract_activity_types(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        recording = False
        for line in file:
            line = line.strip()
            if line.startswith("@Begin"):
                recording = True
                continue
            if not recording or line.startswith(("@", "%")):
                continue

            cleaned_line = clean_line(line)
            if cleaned_line:
                collected_lines.append(cleaned_line)

                # Count sentences for each activity type in this age group
                for act in activities:
                    metadata[age_group]["sentences"][act] += 1

    print(f"Processed: {file_path}")


""" Main Execution """
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter CHILDES .cha files based on child age.")
    parser.add_argument("min_age", type=int, help="Minimum child age in months")
    parser.add_argument("max_age", type=int, help="Maximum child age in months")

    args = parser.parse_args()

    filtered_files = find_cha_files(data_folder, args.min_age, args.max_age)
    print(f"Found {len(filtered_files)} files for age range {args.min_age}-{args.max_age} months.")

    collected_lines = []
    for file_path in filtered_files:
        age_group = extract_age_from_file(file_path)
        if age_group is not None:
            process_chat_files(file_path, collected_lines, age_group)

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"age_{args.min_age}_{args.max_age}.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(collected_lines))

    print(f"Processed data saved to {output_file}")

    """ Generate Metadata Output """
    metadata_output = os.path.join(output_folder, f"metadata_{args.min_age}_{args.max_age}.csv")
    metadata_list = []

    for age, data in sorted(metadata.items()):
        total_sentences = sum(data["sentences"].values())
        for act, count in data["sentences"].items():
            percentage = (count / total_sentences * 100) if total_sentences > 0 else 0
            metadata_list.append({
                "Age (Months)": age,
                "File Count": data["file_count"],
                "Activity Type": act,
                "Sentence Count": count,
                "Percentage": round(percentage, 2)
            })

    df_metadata = pd.DataFrame(metadata_list)
    df_metadata.to_csv(metadata_output, index=False)

    print(f"Metadata saved to {metadata_output}")