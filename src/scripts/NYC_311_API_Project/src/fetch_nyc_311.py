import requests
import pandas as pd
import time
import os

def fetch_nyc_311(limit_per_request=1000, total_records=10000, save_path="../data/nyc_311_complaints.csv"):
    base_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    all_data = []

    for offset in range(0, total_records, limit_per_request):
        print(f"\nRequesting rows {offset} to {offset + limit_per_request}...")

        params = {
            "$limit": limit_per_request,
            "$offset": offset,
            "$order": "created_date DESC"
        }

        # Retry logic for 503 errors
        for attempt in range(5):
            response = requests.get(base_url, params=params)
            
            print(f"Status code: {response.status_code}")
            print(f"Content-Length: {response.headers.get('Content-Length')}")
            print(f"Rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")
            print(f"Request attempt: {attempt + 1}")

            if response.status_code == 200:
                break
            elif response.status_code == 503:
                wait_time = 2 ** attempt
                print(f"503 Service Unavailable. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            elif response.status_code == 429:
                print("429 Too Many Requests. You are being rate limited.")
                print(f"Headers: {response.headers}")
                break
            else:
                print(f"Unexpected error. Status code: {response.status_code}")
                print("Response preview:", response.text[:300])
                break

        if response.status_code != 200:
            continue

        try:
            chunk = response.json()
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            break

        print(f"Records returned: {len(chunk)}")

        if not chunk:
            print("No more data returned by the API.")
            break

        all_data.extend(chunk)
        time.sleep(0.2)

    if all_data:
        df = pd.DataFrame(all_data)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        print(f"\nSaved {len(df)} rows to {save_path}")
        return df
    else:
        print("\nNo data fetched. Nothing saved.")
        return pd.DataFrame()


if __name__ == "__main__":
    print("Running fetch_nyc_311 as standalone script.")
    fetch_nyc_311()
