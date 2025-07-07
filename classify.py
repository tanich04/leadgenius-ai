# classify.py

from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

LABELS = [
    "SaaS", "FinTech", "Healthcare", "E-commerce", "AI", "EdTech",
    "Logistics", "B2B", "DevTools", "Marketing", "HR Tech", "Cybersecurity"
]

def classify_industry(text):
    try:
        result = classifier(text, LABELS)
        top_label = result["labels"][0]
        score = round(result["scores"][0] * 100, 2)
        return top_label, score
    except Exception as e:
        print("[ERROR] Classification failed:", e)
        return "Unknown", 0.0
