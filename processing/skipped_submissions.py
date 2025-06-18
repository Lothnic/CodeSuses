import requests
import pandas as pd
import time

target_verdict = "SKIPPED"

df = pd.read_csv('filtered_users.csv')

if 'cheating' not in df.columns:
    df['cheating'] = False

handles = df['handle'].tolist()
total = len(handles)

for i, handle in enumerate(handles):
    success = False

    for attempt in range(3):
        try:
            response = requests.get(
                f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000",
            )
            response.raise_for_status()
            try:
                data = response.json()
                success = True
                break
            except requests.exceptions.JSONDecodeError:
                print(f"JSON decode failed for handle {handle}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {handle} on attempt {attempt+1}: {e}")
            time.sleep(1)

    if not success:
        print(f"Skipping handle {handle} after 3 failed attempts.")
        continue

    if data.get('status') == 'OK':
        has_skipped = any(sub.get('verdict') == target_verdict for sub in data['result'])
        df.loc[df['handle'] == handle, 'cheating'] = has_skipped
        if has_skipped:
            print(f"Marked {handle} as cheating. {i/total*100}% done.")
    else:
        print(f"API returned non-OK for {handle}: {data}")

    time.sleep(0.01)

df.to_csv('enhanced_filtered_users.csv', index=False)
print("✅ All done! Saved to enhanced_filtered_users.csv")