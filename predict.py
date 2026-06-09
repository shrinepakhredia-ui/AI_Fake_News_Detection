import time
import joblib
from datetime import datetime

from config import (
    RANDOM_FOREST_MODEL,
    TFIDF_MODEL,
)

from src.preprocessing import clean_text


# Load Trained Objects

print("Loading Trained Model...")

model = joblib.load(RANDOM_FOREST_MODEL)

print("Loading TF-IDF Vectorizer...")

vectorizer = joblib.load(TFIDF_MODEL)

feature_names = vectorizer.get_feature_names_out()

print("Model Loaded Successfully")


# Prediction Function

def predict_news(news_text):
    """
    Predict whether the given news article is Real or Fake.

    Returns
    -------
    dict
        prediction
        confidence
        fake_probability
        real_probability
        raw_prediction
        word_count
        character_count
        reading_time
        prediction_time
        processing_time
        risk_level
        explanation
    """

    start_time = time.time()

    try:


        # Validate Input

        if not isinstance(news_text, str):
            raise TypeError("Input must be a string.")

        if not news_text.strip():

            return {

                "prediction": "No Input",

                "confidence": 0,

                "fake_probability": 0,

                "real_probability": 0,

                "raw_prediction": -1,

                "word_count": 0,

                "character_count": 0,

                "reading_time": 0,

                "prediction_time": None,

                "processing_time": 0,

                "risk_level": "Unknown",

                "explanation": "Please enter a valid news article."

            }


        # Article Statistics

        word_count = len(news_text.split())

        character_count = len(news_text)

        reading_time = max(1, round(word_count / 200))


        # Text Cleaning

        cleaned_text = clean_text(news_text)


        # TF-IDF Features

        news_vector = vectorizer.transform([cleaned_text])

        feature_array = news_vector.toarray()[0]

        top_indices = feature_array.argsort()[-5:][::-1]

        top_keywords = []

        for index in top_indices:

            if feature_array[index] > 0:

                top_keywords.append(

                    feature_names[index].title()

                )


        # Prediction

        prediction = model.predict(news_vector)[0]

        probabilities = model.predict_proba(news_vector)[0]

        fake_probability = probabilities[0] * 100

        real_probability = probabilities[1] * 100

        confidence = max(fake_probability, real_probability)


        # Prediction Label

        if prediction == 1:

            label = "✅ REAL NEWS"

        else:

            label = "❌ FAKE NEWS"


        # Risk Level

        if confidence >= 95:

            risk_level = "🟢 Very Low"

        elif confidence >= 85:

            risk_level = "🟡 Low"

        elif confidence >= 70:

            risk_level = "🟠 Medium"

        else:

            risk_level = "🔴 High"


        # Model Explanation

        if prediction == 1:

            explanation = (
                "The article contains language patterns that are "
                "similar to factual and genuine news articles."
            )

        else:

            explanation = (
                "The article contains language patterns commonly "
                "found in fake or misleading news content."
            )


        # Processing Time

        processing_time = round(

            time.time() - start_time,

            4

        )


        # Return Result

        return {

            "prediction": label,

            "confidence": round(confidence, 2),

            "fake_probability": round(fake_probability, 2),

            "real_probability": round(real_probability, 2),

            "raw_prediction": int(prediction),

            "word_count": word_count,

            "character_count": character_count,

            "reading_time": reading_time,

            "prediction_time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            "processing_time": processing_time,

            "risk_level": risk_level,

            "explanation": explanation,

            "top_keywords": top_keywords

        }

    except Exception as e:

        return {

            "prediction": "Prediction Failed",

            "confidence": 0,

            "fake_probability": 0,

            "real_probability": 0,

            "raw_prediction": -1,

            "word_count": 0,

            "character_count": 0,

            "reading_time": 0,

            "prediction_time": None,

            "processing_time": 0,

            "risk_level": "Unknown",

            "top_keywords": [],

            "explanation": "Prediction could not be completed.",

            "error": str(e)

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

    print("\nArticle Statistics")
    print(f"Words : {result['word_count']}")
    print(f"Characters : {result['character_count']}")
    print(f"Reading Time : {result['reading_time']} min")

    print("\nPrediction Details")
    print(f"Risk Level : {result['risk_level']}")
    print(f"Processing Time : {result['processing_time']} sec")
    print(f"Prediction Time : {result['prediction_time']}")

    print("\nModel Explanation")
    print(result["explanation"])

    if "error" in result:
        print(f"\nError : {result['error']}")

    print("=" * 60)