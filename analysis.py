import pandas as pd
from pathlib import Path

# Find CSV files in the data folder
data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    print("No CSV file found in the data folder.")
    print("Please place your dataset inside the data folder.")
    raise SystemExit

# Load the first CSV file
file_path = csv_files[0]

df = pd.read_csv(file_path)

print("\nDATASET LOADED SUCCESSFULLY")
print("-" * 40)

print("File:", file_path.name)

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nBasic statistical summary:")
print(df.describe(include="all").T)

# Save an initial inspection report
report_path = Path("data_inspection.txt")

with open(report_path, "w", encoding="utf-8") as report:
    report.write("CARE TRANSITION ANALYTICS\n")
    report.write("=" * 40 + "\n\n")

    report.write(f"Dataset: {file_path.name}\n")
    report.write(f"Rows: {df.shape[0]}\n")
    report.write(f"Columns: {df.shape[1]}\n\n")

    report.write("Column names:\n")
    report.write(str(df.columns.tolist()) + "\n\n")

    report.write("Missing values:\n")
    report.write(df.isnull().sum().to_string() + "\n\n")

    report.write("Duplicate rows:\n")
    report.write(str(df.duplicated().sum()) + "\n\n")

    report.write("Statistical summary:\n")
    report.write(df.describe(include="all").T.to_string())

print("\nInspection report saved as data_inspection.txt")