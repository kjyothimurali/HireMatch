import pandas as pd

df = pd.read_csv("../data/cleaned_dataset_v2.csv")

# Check duplicates
print("Duplicates:", df.duplicated().sum())

# Check title diversity
print("Unique titles:", df['Title'].nunique())

# Check most frequent titles
print(df['Title'].value_counts().head(10))

# Check description length
print(df['JobDescription'].str.len().describe())