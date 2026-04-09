import torch
import numpy as np
from transformers import DistilBertForSequenceClassification, AutoTokenizer
torch.set_num_threads(1)


MODEL_NAME = "jyothimurali/hirematch-model"

model = None
tokenizer = None

# Labels
labels = ["Finance", "Healthcare", "IT", "Sales & Marketing"]


def load_model():
    global model, tokenizer

    if model is None:
        print("🔄 Loading model from HuggingFace...")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = DistilBertForSequenceClassification.from_pretrained(
            MODEL_NAME,
            low_cpu_mem_usage=True 
        )

        model.eval()
        print(" Model loaded successfully!")


# 🔍 Prediction function
def predict_sector(text):
    try:
        load_model()  

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1).cpu().numpy()[0]

        max_prob = np.max(probs)

        # Confidence threshold
        if max_prob < 0.3:
            return "Other / Unknown"

        return labels[np.argmax(probs)]

    except Exception as e:
        print("PREDICTION ERROR:", e)
        return "Error"


# -------- TEST --------
if __name__ == "__main__":
    text = "Software engineer with Python and machine learning experience"
    print(predict_sector(text))