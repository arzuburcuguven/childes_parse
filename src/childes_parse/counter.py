import argparse

folder_path = "../../data/PARSED/age"

def frag_sent_counter(min_age: int, max_age:int):
    file_path = f"{folder_path}_{min_age}_{max_age}.parsed"
    print(file_path)
    frag_count = 0
    sent_count = 0
    with open(file_path, "r", encoding="utf_8") as file:
        for line in file:
            if line.startswith("(S "):
                sent_count += 1
            else:
                frag_count += 1
    return sent_count, frag_count

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Count the fragments and")
    parser.add_argument("min_age", type=int, help="Minimum child age in months")
    parser.add_argument("max_age", type=int, help="Maximum child age in months")

    # Parse arguments
    args = parser.parse_args()
    sent_count, frag_count = frag_sent_counter(args.min_age, args.max_age)
    print(f"for ages {args.min_age} - {args.max_age} sentence_count: {sent_count} fragment count: {frag_count}")

