
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "Data/sleep_dataset.xlsx"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

df = pd.read_excel(DATA_FILE)
df.columns = df.columns.astype(str).str.strip()

df = df.drop(
    columns=["Stress Level", "Person ID"],
    errors="ignore"
)

print("\nDataset Information:")
df.info()

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

if "Sleep Disorder" in df.columns:
    print("\nSleep Disorder Distribution:")
    print(df["Sleep Disorder"].value_counts(dropna=False))

if "Sleep Duration" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Sleep Duration"].dropna(), bins=10, kde=True)
    plt.title("Sleep Duration Distribution")
    plt.xlabel("Sleep Duration")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

if "Sleep Disorder" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Sleep Disorder")
    plt.title("Sleep Disorder Distribution")
    plt.xlabel("Sleep Disorder")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

if "Sleep Duration" in df.columns and "Quality of Sleep" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="Sleep Duration",
        y="Quality of Sleep",
        hue="Sleep Disorder" if "Sleep Disorder" in df.columns else None
    )
    plt.title("Sleep Duration vs Sleep Quality")
    plt.tight_layout()
    plt.show()

numeric_data = df.select_dtypes(include="number")

if len(numeric_data.columns) >= 2:
    plt.figure(figsize=(10, 7))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
    plt.title("Numeric Feature Correlation")
    plt.tight_layout()
    plt.show()
