
import pandas as pd
sector_keywords = {
    "IT": [
        "software", "developer", "programmer", "java", "python",
        "web", "data", "database", "network", "it ", "system", "backend", "frontend", "cloud"
    ],

    "Finance": [
        "account", "finance", "bank", "audit", "tax",
        "financial", "budget", "payroll", "accountant"
    ],

    "Healthcare": [
        "medical", "doctor", "nurse", "pharma",
        "hospital", "clinic", "health", "patient"
    ],

    "Sales & Marketing": [
        "sales", "marketing", "seo", "brand",
        "business development", "advertising", "client"
    ],
}

def assign_sector(text):
    text = str(text).lower()

    scores = {sector: 0 for sector in sector_keywords}

    for sector, keywords in sector_keywords.items():
        for word in keywords:
            if word in text:
                scores[sector] += 1

    best_sector = max(scores, key=scores.get)

    
    if scores[best_sector] < 3:
        return "Other"

    return best_sector

df = pd.read_csv("../data/merged_dataset.csv")

df['text'] = df['Title'] * 4 + " " + df['JobDescription']
df['sector'] = df['text'].apply(assign_sector)

# REMOVE NOISE
df = df[df['sector'] != "Other"]

df.to_csv("../data/labeled_dataset.csv", index=False)

print(df['sector'].value_counts())