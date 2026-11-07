
import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("model", "sleep_prediction_model.pkl")


def predict_sleep(input_data):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model not found. Run train_model.py first."
        )

    model = joblib.load(MODEL_PATH)

    if not isinstance(input_data, (dict, pd.DataFrame)):
        raise TypeError(
            "Input must be a dictionary or pandas DataFrame."
        )

    if isinstance(input_data, dict):
        input_df = pd.DataFrame([input_data])
    else:
        input_df = input_data.copy()

    input_df.columns = input_df.columns.astype(str).str.strip()

    if not hasattr(model, "feature_names_in_"):
        raise ValueError(
            "The saved model has no feature names. "
            "Retrain the model using the corrected train_model.py."
        )

    expected_columns = list(model.feature_names_in_)
    input_df = input_df.reindex(columns=expected_columns)

    # Check that categorical columns are not passed to
    # the numeric median imputer.
    if hasattr(model, "named_steps"):
        preprocessing = model.named_steps.get("preprocessing")

        if preprocessing is None:
            preprocessing = model.named_steps.get("preprocessor")

        if preprocessing is None:
            raise ValueError(
                "The saved model has no expected preprocessing step. "
                "Retrain the model."
            )

        transformers = getattr(preprocessing, "transformers_", [])

        numeric_columns = []
        categorical_columns = []

        for name, transformer, columns in transformers:
            if name == "remainder":
                continue
            if isinstance(columns, (list, tuple)):
                if name.lower() == "numeric":
                    numeric_columns.extend(columns)
                elif name.lower() == "categorical":
                    categorical_columns.extend(columns)

        if "Gender" in numeric_columns:
            raise ValueError(
                "Gender is configured as numeric in the saved model. "
                "Replace train_model.py and retrain the model."
            )

        if "Gender" in expected_columns and "Gender" not in categorical_columns:
            raise ValueError(
                "Gender is not configured as categorical. "
                "Retrain the model with the corrected preprocessing."
            )

    prediction = model.predict(input_df)[0]

    confidence = 0.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        confidence = float(probabilities.max() * 100)

    return prediction, confidence
