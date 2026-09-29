
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# ==========================================
# 1. Load Dataset
# ==========================================

DATASET = "network_configure.csv"

df = pd.read_csv(DATASET)

print("Dataset shape:", df.shape)

print("\nIntent distribution:")
print(df["intent"].value_counts())


# ==========================================
# 2. Remove extremely rare classes
# ==========================================

MIN_SAMPLES = 2

class_counts = df["intent"].value_counts()

valid_classes = class_counts[
    class_counts >= MIN_SAMPLES
].index

removed_classes = class_counts[
    class_counts < MIN_SAMPLES
].index

if len(removed_classes) > 0:

    print("\nWarning: Removing classes with fewer than 2 samples:")

    for cls in removed_classes:
        print(" -", cls)

    df = df[
        df["intent"].isin(valid_classes)
    ].copy()


# ==========================================
# 3. Features and labels
# ==========================================

X = df["command"].astype(str)
y = df["intent"].astype(str)


# ==========================================
# 4. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 5. NLP Pipeline
# ==========================================

model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(

            lowercase=True,

            ngram_range=(1, 3),

            sublinear_tf=True,

            analyzer="word"
        )
    ),

    (
        "classifier",

        LogisticRegression(

            max_iter=3000,

            class_weight="balanced"
        )
    )
])


# ==========================================
# 6. Train
# ==========================================

print("\nTraining NLP model...")

model.fit(
    X_train,
    y_train
)


# ==========================================
# 7. Evaluate
# ==========================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print(
    "Accuracy:",
    round(accuracy, 4)
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ==========================================
# 8. Save Model
# ==========================================

MODEL_PATH = "nlp_model.pkl"

joblib.dump(
    model,
    MODEL_PATH
)

print("\n================================")
print("MODEL SAVED")
print("================================")

print(
    f"Model saved to: {MODEL_PATH}"
)
X = df["command"].astype(str)
y = df["intent"]


# ---------------------------------------
# 3. Train/Test split
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ---------------------------------------
# 4. NLP Pipeline
# ---------------------------------------

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 3),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])


# ---------------------------------------
# 5. Train
# ---------------------------------------

model.fit(X_train, y_train)


# ---------------------------------------
# 6. Evaluate
# ---------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ---------------------------------------
# 7. Save model
# ---------------------------------------

joblib.dump(
    model,
    "nlp_model.pkl"
)

print("\nModel saved as nlp_model.pkl")