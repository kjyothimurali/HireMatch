import pandas as pd

# Load dataset
df = pd.read_csv("../data/data job posts.csv")

# Keep only important columns
df = df[['Title', 'JobDescription']]

# Remove missing values
df = df.dropna(subset=['Title', 'JobDescription'])

# Remove very small descriptions (noise)
df = df[df['JobDescription'].str.len() > 100]

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv("../data/cleaned_dataset.csv", index=False)

print("Cleaned dataset size:", len(df))
print(df.head())
df = pd.read_csv("../data/cleaned_dataset.csv")

df = df.drop_duplicates()

df.to_csv("../data/cleaned_dataset_v2.csv", index=False)

print("New size:", len(df))