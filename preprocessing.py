
import pandas as pd


def split_blood_pressure(value):
    try:
        parts = str(value).strip().split("/")
        if len(parts) != 2:
            return None, None

        return float(parts[0]), float(parts[1])
    except (ValueError, TypeError):
        return None, None


def convert_time_to_minutes(value):
    if pd.isna(value):
        return float("nan")

    if isinstance(value, (int, float)):
        # Excel time values are fractions of one day.
        if 0 <= value < 1:
            return value * 1440
        return float(value)

    text = str(value).strip()

    for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p"):
        try:
            parsed = pd.to_datetime(text, format=fmt)
            return parsed.hour * 60 + parsed.minute
        except (ValueError, TypeError):
            continue

    return float("nan")


def preprocess_input(data):
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    else:
        data = data.copy()

    data.columns = data.columns.astype(str).str.strip()

    data = data.drop(
        columns=["Stress Level", "Person ID"],
        errors="ignore"
    )

    if "Blood Pressure" in data.columns:
        bp_values = data["Blood Pressure"].apply(split_blood_pressure)

        data["Systolic BP"] = bp_values.apply(lambda x: x[0])
        data["Diastolic BP"] = bp_values.apply(lambda x: x[1])

        data = data.drop(columns=["Blood Pressure"])

    for column in ["Sleep Start Time", "Wake-up Time"]:
        if column in data.columns:
            data[column] = data[column].apply(convert_time_to_minutes)

    return data
