import pandas as pd
import numpy as np
import json
import warnings

warnings.filterwarnings("ignore")

def clean_311_data(df):
    print("Starting NYC 311 data cleaning...")
    print(f"Original shape: {df.shape}\n")

    # Step 1: Drop columns with >80% missing (log), then drop those >90%
    missing = df.isnull().mean()
    high_missing = missing[missing > 0.8].sort_values(ascending=False)

    if not high_missing.empty:
        print("Columns with >80% missing values (to inspect):")
        print(high_missing, "\n")

    cols_to_drop = missing[missing > 0.9].index.tolist()
    df.drop(columns=cols_to_drop, inplace=True)
    print(f"Dropped {len(cols_to_drop)} columns with >90% missing data.")
    print(f"New shape after column drop: {df.shape}\n")

    # Step 2: Fill categorical values with "Unknown"
    cat_cols = ['borough', 'complaint_type', 'descriptor', 'location_type']
    for col in cat_cols:
        if col in df.columns:
            if pd.api.types.is_categorical_dtype(df[col]):
                if "Unknown" not in df[col].cat.categories:
                    df[col] = df[col].cat.add_categories("Unknown")
            df[col] = df[col].fillna("Unknown")
    print(f"Filled missing values in categorical columns: {cat_cols}")

    # Step 3: Parse datetime fields
    df['created_date'] = pd.to_datetime(df.get('created_date'), errors='coerce')
    df['closed_date'] = pd.to_datetime(df.get('closed_date'), errors='coerce')
    print("Standardized 'created_date' and 'closed_date' columns.")

    # Step 4: Time-based features
    df['response_time'] = (df['closed_date'] - df['created_date']).dt.total_seconds() / 3600
    df['day_of_week'] = df['created_date'].dt.day_name()
    df['hour'] = df['created_date'].dt.hour
    print("Added 'response_time', 'day_of_week', and 'hour' columns.")

    # Step 5: Clean zip codes
    if 'incident_zip' in df.columns:
        df['incident_zip'] = df['incident_zip'].astype(str).str.zfill(5)
        df['incident_zip'] = df['incident_zip'].replace("nan", "Unknown")
        print("Cleaned 'incident_zip' column.")

    # Step 6: Convert to category dtype
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    print("Converted categorical columns to 'category' dtype.")

    # Step 7: Clean latitude & longitude, drop missing
    df['latitude'] = pd.to_numeric(df.get('latitude'), errors='coerce')
    df['longitude'] = pd.to_numeric(df.get('longitude'), errors='coerce')
    before_geo = df.shape[0]
    df = df.dropna(subset=['latitude', 'longitude'])
    print(f"Dropped {before_geo - df.shape[0]} rows missing latitude or longitude.")

    # Step 8: Clean selected text fields
    text_cols = ['incident_address', 'descriptor']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", "Unknown")
    print(f"Cleaned text fields: {text_cols}")

    # Step 9: Flatten columns with nested dictionaries
    dict_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()]
    for col in dict_cols:
        expanded = df[col].apply(pd.Series).add_prefix(f"{col}_")
        df = pd.concat([df.drop(columns=[col]), expanded], axis=1)

    if dict_cols:
        print(f"Flattened dict-type columns: {dict_cols}")
        print("Example of expanded nested structure:")
        example_data = {
            "latitude": "40.7558",
            "longitude": "-73.9864",
            "human_address": {
                "address": "123 Main St",
                "city": "New York"
            }
        }
        print(json.dumps(example_data, indent=2))

    # Step 10: Drop duplicate rows
    before_dedup = df.shape[0]
    df = df.drop_duplicates()
    print(f"Removed {before_dedup - df.shape[0]} duplicate rows.")

    print(f"\nCleaning complete. Final shape: {df.shape}")
    return df
