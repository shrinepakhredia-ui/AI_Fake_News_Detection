import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from config import (
    PROCESSED_DATASET,
    TFIDF_MODEL,
    MAX_FEATURES,
    STOP_WORDS
)


def extract_features():

    print("=" * 60)
    print("Loading Processed Dataset...")
    print("=" * 60)

    # Load Dataset
    df = pd.read_csv(PROCESSED_DATASET)

    print("Dataset Loaded Successfully")
    print("Dataset Shape :", df.shape)

    # Handle Missing Values


    df["content"] = df["content"].fillna("").astype(str)

    # Remove Empty Rows

    df = df[df["content"].str.strip() != ""]

    print("Valid Samples :", len(df))

    # Features & Labels


    X = df["content"]

    y = df["label"]

    # TF-IDF


    print("\nApplying TF-IDF...")

    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        stop_words=STOP_WORDS
    )

    X = vectorizer.fit_transform(X)

    print("TF-IDF Applied Successfully")
    print("Feature Matrix Shape :", X.shape)

    # Save Vectorizer

    joblib.dump(vectorizer, TFIDF_MODEL)

    print("\nTF-IDF Vectorizer Saved Successfully")
    print(TFIDF_MODEL)

    return X, y


if __name__ == "__main__":

    extract_features()