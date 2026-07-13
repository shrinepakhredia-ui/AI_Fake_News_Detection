import time
import joblib
from datetime import datetime
from src.source_score import get_source_score

from config import (
    RANDOM_FOREST_MODEL,
    TFIDF_MODEL,
)

from src.preprocessing import clean_text
from src.source_checker import check_source



# Load Trained Objects

print("Loading Trained Model...")

model = joblib.load(RANDOM_FOREST_MODEL)

print("Loading TF-IDF Vectorizer...")

vectorizer = joblib.load(TFIDF_MODEL)

feature_names = vectorizer.get_feature_names_out()

print("Model Loaded Successfully")



# Prediction Function

def predict_news(news_text, source_url=None):
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
        trust_score
        trusted_source
        publisher
        trust_reasons
        top_keywords
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

                "explanation": "Please enter a valid news article.",

                "top_keywords": [],

                "trust_score": 0,

                "trusted_source": False,

                "publisher": "Unknown",

                "authenticity_score": 0,

                "authenticity_level": "Unknown",

                "trust_reasons": []

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

        # AI Explanation

        if prediction == 1:

            explanation = f"""
        ### ✅ AI Assessment

        The model predicts that this article is **likely genuine**.

        ### Why?

        • Writing style matches trusted news patterns.

        • Language appears balanced and objective.

        • No strong misleading linguistic signals were detected.

        • Source reliability and article structure support authenticity.

        ### Recommendation

        You can consider this article **reliable**, but always cross-check important information with multiple trusted publishers.
        """

        else:

            explanation = f"""
        ### 🚨 AI Assessment

        The model predicts that this article is **likely fake or misleading**.

        ### Why?

        • Sensational or emotionally charged wording was detected.

        • Writing pattern differs from verified news articles.

        • Low source credibility or suspicious language indicators were found.

        • Prediction confidence suggests possible misinformation.

        ### Recommendation

        Avoid sharing this article until it has been verified by trusted news organizations.
        """

        # AI Verdict Summary

        if prediction == 1:

            verdict = (
                f"This article is likely authentic with a confidence of "
                f"{round(confidence,1)}%. "
                f"The writing style resembles genuine journalism "
                f"and no major misinformation patterns were detected."
            )

        else:

            verdict = (
                f"This article appears suspicious with a confidence of "
                f"{round(confidence,1)}%. "
                f"The model detected linguistic patterns commonly "
                f"associated with fake or misleading news."
            )
        # Source Verification

        source_info = {

            "trusted": False,

            "publisher": "Unknown",

            "domain": ""

        }

        #Source Verification

        trusted_source = False

        publisher="Unknown"

        source_info = {

            "trusted" : False,

            "publisher": "Unknown"
        }

        if source_url:

            source_info = check_source(source_url)

            trusted_source = source_info["trusted"]

            publisher = source_info["publisher"]

        # Source Reliability Score

        source_data = get_source_score(publisher)

        source_score = source_data["score"]

        source_level = source_data["level"]


        # AI Trust Score


        trust_score = confidence

        trust_reasons = []

        # Trusted Publisher Bonus

        if source_info["trusted"]:

            trust_score += 15

            trust_reasons.append(

                f"Trusted Publisher ({source_info['publisher']})"

            )

        # Long Article Bonus

        if word_count >= 300:

            trust_score += 5

            trust_reasons.append(

                "Detailed Article"

            )

        # Very Short Article Penalty

        elif word_count < 80:

            trust_score -= 10

            trust_reasons.append(

                "Very Short Article"

            )

        # High Confidence Bonus

        if confidence >= 95:

            trust_score += 5

            trust_reasons.append(

                "High ML Confidence"

            )

        # Medium Confidence

        elif confidence >= 80:

            trust_reasons.append(

                "Good ML Confidence"

            )

        else:

            trust_reasons.append(

                "Low ML Confidence"

            )

        # Clamp Score

        trust_score = max(

            0,

            min(

                100,

                round(trust_score, 2)

            )

        )

        #Overall News Authenticity Score

        authenticity_score = (

            (confidence * 0.45)

            +

            (trust_score * 0.35)

            +

            (source_score * 0.20)

        )

        authenticity_score = round(

            min(100, authenticity_score),

            2

        )

        if authenticity_score >= 90:

            authenticity_level = "Highly Authentic"

        elif authenticity_score >=75:

            authenticity_level = "Likely Authentic"

        elif authenticity_score >=60:

            authenticity_level = "Needs Verification"

        else:

            authenticity_level = "Suspicious"


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

            "top_keywords": top_keywords,

            "trust_score": trust_score,

            "trusted_source": trusted_source,

            "publisher": publisher,

            "trust_reasons": trust_reasons,

            "source_score": source_score,

            "source_level": source_level,

            "authenticity_score": authenticity_score,

            "authenticity_level": authenticity_level,

            "ai_verdict": verdict,

            "confidence_label": (
                "Very High" if confidence >= 95 else
                "High" if confidence >= 85 else
                "Medium" if confidence >= 70 else
                "Low"
            ),

            "ai_verdict": (
                "Highly Reliable"
                if authenticity_score >= 90
                else
                "Likely Genuine"
                if authenticity_score >= 75
                else
                "Needs Verification"
                if authenticity_score >= 60
                else
                "Potential Misinformation"
            ),

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

            "trust_score": 0,

            "trusted_source": False,

            "publisher": "Unknown",

            "trust_reasons": [],

            "explanation": "Prediction could not be completed.",

            "authenticity_score": 0,

            "authenticity_level": "Unknown",

            "confidence_label": "Unknown",

            "ai_verdict": "Unknown",

            "error": str(e)

        }



# Testing


if __name__ == "__main__":

    print("=" * 60)

    news = input("Enter News Article:\n\n")

    result = predict_news(news)

    print("\nPrediction :", result["prediction"])

    print(f"Confidence : {result['confidence']} %")

    print(f"Trust Score : {result['trust_score']} %")

    print(f"Publisher : {result['publisher']}")

    print(f"Trusted Source : {result['trusted_source']}")

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

    print("\nTop Keywords")

    if result["top_keywords"]:

        print(", ".join(result["top_keywords"]))

    else:

        print("No significant keywords detected.")

    print("\nTrust Factors")

    for reason in result["trust_reasons"]:

        print("-", reason)

    print("\nModel Explanation")

    print(result["explanation"])

    if "error" in result:

        print("\nError :", result["error"])

    print("=" * 60)