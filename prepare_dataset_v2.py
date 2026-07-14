import pandas as pd

from config import (
    FAKE_DATASET,
    TRUE_DATASET
)

print("="*60)
print("Loading ISOT Dataset")
print("="*60)

fake_df = pd.read_csv(FAKE_DATASET)
true_df = pd.read_csv(TRUE_DATASET)

fake_df["label"] = 0
true_df["label"] = 1

fake_df["title"] = fake_df["title"].fillna("")
fake_df["text"] = fake_df["text"].fillna("")

true_df["title"] = true_df["title"].fillna("")
true_df["text"] = true_df["text"].fillna("")

fake_df = fake_df[["title","text","label"]]
true_df = true_df[["title","text","label"]]

print("ISOT Loaded Successfully")

print()

print("="*60)
print("Loading WELFake Dataset")
print("="*60)

wel_df = pd.read_csv("data/raw/WELFake_Dataset.csv")

wel_df["label"] = 1 - wel_df["label"]

wel_df = wel_df.drop(columns=["Unnamed: 0"])

wel_df["title"] = wel_df["title"].fillna("")
wel_df["text"] = wel_df["text"].fillna("")

wel_df = wel_df[["title","text","label"]]

print("WELFake Loaded Successfully")

print()

print("ISOT Samples :", len(fake_df)+len(true_df))
print("WELFake Samples :", len(wel_df))

print()
print("=" * 60)
print("Merging Datasets...")
print("=" * 60)

df = pd.concat(

    [fake_df, true_df, wel_df],

    ignore_index=True

)

print("Merged Shape :", df.shape)

print()
print("Removing Empty Articles...")

df = df[

    (df["title"].str.strip() != "")

    |

    (df["text"].str.strip() != "")

]

print("Remaining :", len(df))

print()

print("Creating Content Column...")

df["content"] = (

    df["title"]

    +

    " "

    +

    df["text"]

)

print()

print("Removing Duplicate Articles...")

before = len(df)

df = df.drop_duplicates(

    subset=["content"]

)

after = len(df)

print(

    "Duplicates Removed :",

    before - after

)

print(

    "Remaining Samples :",

    after

)

print()

print("Shuffling Dataset...")

df = df.sample(

    frac=1,

    random_state=42

).reset_index(

    drop=True

)

print("Done.")

from config import PROCESSED_DATASET

df.to_csv(

    PROCESSED_DATASET,

    index=False

)

print()

print("="*60)

print("Dataset Saved Successfully")

print(PROCESSED_DATASET)

print("="*60)