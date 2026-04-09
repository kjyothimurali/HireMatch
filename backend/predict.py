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
        print("🔄 Loading model...")

        try:
            model = DistilBertForSequenceClassification.from_pretrained(
                MODEL_NAME,
                low_cpu_mem_usage=True   # 🔥 VERY IMPORTANT
            )
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

            model.eval()

            print("✅ Model loaded")

        except Exception as e:
            print("MODEL LOAD ERROR:", e)
            return False

    return True
# 🔍 Prediction function
def predict_sector(text):
    if not load_model():
        return "Model failed to load"

    try:
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

        if np.max(probs) < 0.5:
            return "Other / Unknown"

        return labels[np.argmax(probs)]

    except Exception as e:
        print("PREDICTION ERROR:", e)
        return "Prediction failed"


# -------- TEST --------
if __name__ == "__main__":
    text = "Software engineer with Python and machine learning experience"
    print(predict_sector(text))