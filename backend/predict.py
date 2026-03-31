import torch
import numpy as np
from transformers import BertForSequenceClassification
from transformers import AutoTokenizer
# Load model
model = BertForSequenceClassification.from_pretrained("models")

tokenizer = AutoTokenizer.from_pretrained("models")
labels = ["Finance", "Healthcare", "IT", "Sales & Marketing"]

def predict_sector(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1).detach().numpy()[0]

    max_prob = np.max(probs)

    # 🔥 Unknown detection
    if max_prob < 0.5:
        return "Other / Unknown"

    return labels[np.argmax(probs)]


# -------- TEST --------
if __name__ == "__main__":
    text = "sample resume"
    print(predict_sector(text))