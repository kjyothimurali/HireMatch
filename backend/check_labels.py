import pandas as pd

df = pd.read_csv('../data/final_dataset.csv')

for sector in df['sector'].unique():
    print("\n======", sector, "======")
    print(df[df['sector'] == sector].sample(5)[['Title', 'JobDescription']])