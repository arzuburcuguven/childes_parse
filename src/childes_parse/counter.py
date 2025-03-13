import argparse
from collections import defaultdict

folder_path = "../../data/PARSED_spacy/PARSED/age"

def count_line_starters(min_age: int, max_age: int):
    file_path = f"{folder_path}_{min_age}_{max_age}.parsed"
    output_file = f"{folder_path}_{min_age}_{max_age}_counts.txt"
    print(f"Processing file: {file_path}")
    
    starter_counts = defaultdict(int)
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("("):
                first_token = line.split()[0].lstrip("(")  # Extract first token and strip '('
                starter_counts[first_token] += 1
    
    with open(output_file, "w", encoding="utf-8") as out_file:
        for key, value in sorted(starter_counts.items()):
            out_file.write(f"{key}: {value}\n")
    
    print(f"Results saved to {output_file}")
    return dict(starter_counts)


if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Count the fragments and")
    parser.add_argument("min_age", type=int, help="Minimum child age in months")
    parser.add_argument("max_age", type=int, help="Maximum child age in months")

    # Parse arguments
    args = parser.parse_args()
    stats_dict = count_line_starters(args.min_age, args.max_age)
    print(f"for ages {args.min_age} - {args.max_age}: {stats_dict}")

