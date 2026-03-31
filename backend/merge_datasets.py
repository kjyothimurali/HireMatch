import pandas as pd
import re

# -------- LOAD DATA --------
df1 = pd.read_csv("../data/cleaned_dataset_v2.csv")
df2 = pd.read_csv("../data/allJobs.csv")

# -------- SELECT CORRECT COLUMNS --------
df2 = df2[['Job-Title', 'Description']]
df2.columns = ['Title', 'JobDescription']

# -------- CLEAN FUNCTION --------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text

# -------- CLEAN BOTH DATASETS --------
df1['Title'] = df1['Title'].apply(clean_text)
df1['JobDescription'] = df1['JobDescription'].apply(clean_text)

df2['Title'] = df2['Title'].apply(clean_text)
df2['JobDescription'] = df2['JobDescription'].apply(clean_text)

# -------- REMOVE NULLS --------
df2 = df2.dropna(subset=['Title', 'JobDescription'])

# -------- FILTER SHORT TEXT --------
df2 = df2[df2['JobDescription'].str.len() > 100]

# -------- MERGE --------
df_all = pd.concat([df1, df2], ignore_index=True)

# -------- REMOVE DUPLICATES --------
df_all = df_all.drop_duplicates(subset=['Title', 'JobDescription'])

# -------- SAVE --------
df_all.to_csv("../data/merged_dataset.csv", index=False)

print("Merged dataset size:", len(df_all))