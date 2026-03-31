import pandas as pd

# Load labeled dataset
df = pd.read_csv("../data/labeled_dataset.csv")

# -------- CHECK DISTRIBUTION --------
print("Before balancing:\n", df['sector'].value_counts())

# -------- BALANCE DATA --------
TARGET = 4000

df_balanced = df.groupby('sector').apply(
    lambda x: x.sample(min(len(x), TARGET), random_state=42)
).reset_index(drop=True)

# -------- SAVE FINAL DATASET --------
df_balanced.to_csv("../data/final_dataset.csv", index=False)

print("\nAfter balancing:\n", df_balanced['sector'].value_counts())
print("\nTotal rows:", len(df_balanced))