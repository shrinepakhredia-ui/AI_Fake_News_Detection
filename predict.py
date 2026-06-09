import joblib

from config import (
    RANDOM_FOREST_MODEL,
    TFIDF_MODEL,
)

from src.preprocessing import clean_text


# Load Saved Objects

print("Loading Trained Model...")

model = joblib.load(RANDOM_FOREST_MODEL)

print("Loading TF-IDF Vectorizer...")

vectorizer = joblib.load(TFIDF_MODEL)

print("Model Loaded Successfully")


# Prediction Function

def predict_news(news_text):

    if not news_text.strip():
        return {
            "prediction": "No Input",
            "confidence": 0,
            "fake_probability": 0,
            "real_probability": 0
        }

    # Clean Input
    news_text = clean_text(news_text)

    # Convert into TF-IDF Features
    news_vector = vectorizer.transform([news_text])

    # Prediction
    prediction = model.predict(news_vector)

    # Prediction Probability
    probability = model.predict_proba(news_vector)

    fake_probability = probability[0][0] * 100
    real_probability = probability[0][1] * 100

    confidence = max(fake_probability, real_probability)

    if prediction[0] == 1:

        label = "✅ REAL NEWS"

    else:

        label = "❌ FAKE NEWS"

    return {
        "prediction": label,
        "confidence": round(confidence, 2),
        "fake_probability": round(fake_probability, 2),
        "real_probability": round(real_probability, 2)
    }


# Testing

if __name__ == "__main__":

    print("=" * 60)

    news = input("Enter News Article:\n\n")

    result = predict_news(news)

    print("\nPrediction :", result["prediction"])
    print(f"Confidence : {result['confidence']} %")
    print(f"Fake Probability : {result['fake_probability']} %")
    print(f"Real Probability : {result['real_probability']} %")

    print("=" * 60)