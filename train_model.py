
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Data", "sleep_dataset.xlsx")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "sleep_prediction_model.pkl")


def main():
    # Load dataset
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_excel(DATA_PATH)
    df.columns = df.columns.astype(str).str.strip()

    # Remove unnecessary columns
    drop_columns = [
        col for col in df.columns
        if col.lower() == "person id"
        or col.lower() == "stress level"
        or col.lower().startswith("unnamed:")
    ]
    df.drop(columns=drop_columns, inplace=True, errors="ignore")

    # Validate target
    target = "Sleep Disorder"
    if target not in df.columns:
        raise ValueError(
            "Sleep Disorder column not found in the dataset."
        )

    df = df.dropna(subset=[target]).copy()

    # Clean string values
    for col in df.columns:
        if (
            pd.api.types.is_object_dtype(df[col])
            or isinstance(df[col].dtype, pd.StringDtype)
        ):
            df[col] = df[col].map(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

    # Separate features and target
    X = df.drop(columns=[target]).copy()
    y = df[target].astype("string").str.strip()

    # Remove empty target labels
    valid_rows = y.notna() & y.ne("")
    X = X.loc[valid_rows].copy()
    y = y.loc[valid_rows].astype(str)

    if len(X) < 5:
        raise ValueError(
            "Not enough valid rows to train the model."
        )

    if y.nunique() < 2:
        raise ValueError(
            "At least two Sleep Disorder classes are required."
        )

    # Explicitly identify known categorical columns
    known_categorical = [
        "Gender",
        "Occupation",
        "BMI Category",
        "Alcohol Consumption",
        "Smoking",
        "Exercise Type",
        "Sleep Start Time",
        "Wake-up Time"
    ]

    for col in known_categorical:
        if col in X.columns:
            X[col] = X[col].astype("string")

    # Automatically identify remaining categorical columns
    categorical_features = X.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    # Identify numeric columns only after categorical conversion
    numerical_features = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    print("Dataset rows:", len(X))
    print("Categorical features:", categorical_features)
    print("Numerical features:", numerical_features)
    print("Target classes:", sorted(y.unique()))

    # Categorical preprocessing
    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )
    ])

    # Numerical preprocessing
    numerical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ])

    # Build preprocessing transformers
    transformers = []

    if categorical_features:
        transformers.append(
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            )
        )

    if numerical_features:
        transformers.append(
            (
                "numerical",
                numerical_pipeline,
                numerical_features
            )
        )

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    # Random Forest pipeline
    model = Pipeline([
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        )
    ])

    # Stratify when every class has at least two records
    class_counts = y.value_counts()
    stratify_target = (
        y
        if len(class_counts) > 1
        and class_counts.min() >= 2
        else None
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify_target
    )

    # Train
    print("\nTraining Random Forest model...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\nTraining completed successfully.")
    print(f"Test accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    # Save the complete pipeline
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\nModel saved successfully:")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()
