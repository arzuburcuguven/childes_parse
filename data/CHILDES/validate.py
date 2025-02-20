import os
import pandas as pd

folder_path = os.path.dirname(__file__) 
# Get folder names (directories) inside folder_path
folder_names = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]


validation_file = pd.read_csv("/Users/argy/workspace/CHILDES/metadata.csv")

# Assuming the column to compare is the first column
column_name = validation_file.columns[0]  # Get the actual column name
match = validation_file[column_name].isin(folder_names)

print(match)