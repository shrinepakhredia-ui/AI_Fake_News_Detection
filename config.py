# Project Paths

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
MODEL_DIR = "models"

FAKE_DATASET = f"{RAW_DATA_DIR}/Fake.csv"
TRUE_DATASET = f"{RAW_DATA_DIR}/True.csv"

PROCESSED_DATASET = f"{PROCESSED_DATA_DIR}/processed_news.csv"

TFIDF_MODEL = f"{MODEL_DIR}/tfidf_vectorizer.pkl"
RANDOM_FOREST_MODEL = f"{MODEL_DIR}/random_forest.pkl"
LOGISTIC_REGRESSION_MODEL = f"{MODEL_DIR}/logistic_regression.pkl"

# Dataset Settings

TEST_SIZE = 0.20

RANDOM_STATE = 42

# TF-IDF Settings

MAX_FEATURES = 10000

STOP_WORDS = "english"

# Random Forest Settings

N_ESTIMATORS = 100

# Streamlit Settings

APP_TITLE = "📰 Fake News Detection "

PAGE_TITLE = "AI Fake News Detection"
