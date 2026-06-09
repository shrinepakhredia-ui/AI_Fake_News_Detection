import pandas as pd

from config import (
    FAKE_DATASET,
    TRUE_DATASET,
    PROCESSED_DATASET,
    RANDOM_STATE,
)

from src.preprocessing import clean_text


# Load Dataset

print("=" * 60)
print("Loading Datasets...")
print("=" * 60)

fake_df = pd.read_csv(FAKE_DATASET)
true_df = pd.read_csv(TRUE_DATASET)

print(f"Fake News : {fake_df.shape}")
print(f"True News : {true_df.shape}")

# Assign Labels

fake_df["label"] = 0
true_df["label"] = 1

print("\nLabels Assigned Successfully")

# Merge Dataset

df = pd.concat([fake_df, true_df], ignore_index=True)

print("Datasets Merged Successfully")
print("Merged Shape :", df.shape)

# Shuffle Dataset

df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print("Dataset Shuffled Successfully")

# Handle Missing Values

print("\nHandling Missing Values...")

df["title"] = df["title"].fillna("").astype(str)
df["text"] = df["text"].fillna("").astype(str)

print("Missing Values Handled Successfully")

# Create Content Column

df["content"] = df["title"] + " " + df["text"]

print("Content Column Created Successfully")

# Clean News Content

print("\nCleaning News Articles...")

df["content"] = df["content"].apply(clean_text)

print("Text Cleaning Completed")

# Remove Empty Articles

df = df[df["content"].str.strip() != ""]

print("Empty Articles Removed")
print("Remaining Samples :", len(df))


# Save Processed Dataset

df.to_csv(PROCESSED_DATASET, index=False)

print("\nProcessed Dataset Saved Successfully")
print(PROCESSED_DATASET)

print("\n" + "=" * 60)
print("Dataset Preparation Completed Successfully")
print("=" * 60)