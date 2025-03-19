# python age-grouped-stats.py metadata_0_12.csv

import pandas as pd
import argparse
import os

input_folder =  "../../data/AOCHILDES"


def compute_age_range_stats(metadata_file):
    # Load metadata CSV
    if not os.path.exists(metadata_file):
        print(f"Error: File {metadata_file} not found.")
        return

    df = pd.read_csv(metadata_file)

    # Aggregate data across all ages in the given range
    total_sentences = df["Sentence Count"].sum()

    # Group by activity type and sum sentence counts
    activity_summary = df.groupby("Activity Type")["Sentence Count"].sum().reset_index()

    # Calculate percentages
    activity_summary["Percentage"] = (activity_summary["Sentence Count"] / total_sentences) * 100

    # Reorder columns
    activity_summary = activity_summary[["Activity Type", "Sentence Count", "Percentage"]]

    # Save results
    output_file = metadata_file.replace("metadata", "age_range_summary")
    activity_summary.to_csv(output_file, index=False)
    print(f"Age range activity statistics saved to {output_file}")

    # Display results interactively
    try:
        import ace_tools as tools
        tools.display_dataframe_to_user(name="Age Range Activity Statistics", dataframe=activity_summary)
    except ImportError:
        print(activity_summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute age-group statistics from metadata CSV.")
    parser.add_argument("metadata_file", type=str, help="Path to metadata CSV file")

    args = parser.parse_args()
    input_file = os.path.join(input_folder, args.metadata_file)
    compute_age_range_stats(input_file)
