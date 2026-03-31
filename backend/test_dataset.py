import pandas as pd

df = pd.read_csv("../data/data job posts.csv")

print(df.head())
print(df.columns)
print("Total rows:", len(df))
print(df.isnull().sum())