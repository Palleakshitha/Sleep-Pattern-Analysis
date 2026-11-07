
import pandas as pd

files = [
    "Data/sleep_dataset.xlsx",
    "Data/sleep_dataset_updated_v2.xlsx"
]

for file in files:
    try:
        df = pd.read_excel(file)
        print("\nFile:", file)
        print(df["Sleep Disorder"].value_counts(dropna=False))
    except FileNotFoundError:
        print("\nFile not found:", file)