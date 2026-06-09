import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from config import (
    RANDOM_FOREST_MODEL,
    RANDOM_STATE,
    TEST_SIZE,
    N_ESTIMATORS,
)


def train_model(X, y):

    print("=" * 60)
    print("Splitting Dataset...")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"Training Samples : {X_train.shape[0]}")
    print(f"Testing Samples  : {X_test.shape[0]}")

    print("\nTraining Random Forest Model...")

    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    print("Model Trained Successfully")

    # Prediction
    predictions = model.predict(X_test)

    # Evaluation Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print("\n" + "=" * 60)
    print("Model Performance")
    print("=" * 60)

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report\n")
    print(classification_report(y_test, predictions))

    print("Confusion Matrix\n")
    print(confusion_matrix(y_test, predictions))

    # Save Model
    joblib.dump(model, RANDOM_FOREST_MODEL)

    print("\nModel Saved Successfully")
    print(RANDOM_FOREST_MODEL)

    return {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


if __name__ == "__main__":

    from src.feature_engineering import extract_features

    X, y = extract_features()

    train_model(X, y)