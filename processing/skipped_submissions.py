import requests
import pandas as pd

# Define the handle and verdict you want to filter by
target_verdict = "SKIPPED"  # The verdict we're looking for

df = pd.read_csv('data/filtered_users.csv')
handles = df['handle'].tolist()

# cheating_handles = list()
i=0
for handle in handles:
    response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000")
    data = response.json()
    i+=1
    if data['status'] == 'OK':
        has_skipped = any(sub.get('verdict') == target_verdict for sub in data['result'])
        if has_skipped:
            # cheating_handles.append(handle)
            df.loc[df['handle'] == handle, 'cheating'] = True
            print(f"Marked {handle} handle as cheating. {i/35612*100}%")
        else:
            df.loc[df['handle'] == handle, 'cheating'] = False

df.to_csv('data/enhanced_filtered_users.csv', index=False)
