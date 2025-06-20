import pandas as pd
import requests

full = pd.read_csv('data/fulldata.csv')
hand = pd.read_csv('data/handles.csv')

fulllist = hand['handles'].astype(str).tolist()
partlist = full['handle'].astype(str).tolist()

remlist = list(set(fulllist) - set(partlist))

details = []
failed = []

for i, handle in enumerate(remlist):
    try:
        response = requests.get(
            f'https://codeforces.com/api/user.info?handles={handle}&checkHistoricHandles=false',
            timeout=10
        )
        data = response.json()

        # ✅ Check status BEFORE accessing result
        if data.get("status") != "OK":
            print(f"❌ API failed for handle {handle}: {data.get('comment', 'No comment')}")
            failed.append(handle)
            continue

        user = data['result'][0]

        details.append({
            "handle": user.get("handle"),
            "rating": user.get("rating"),
            "maxRating": user.get("maxRating"),
            "rank": user.get("rank"),
            "maxRank": user.get("maxRank"),
            "friends": user.get('friendOfCount'),
            "contributions": user.get('contribution'),
            "country": user.get("country"),
            "city": user.get("city"),
            "organization": user.get("organization"),
            "avatar link": user.get('avatar')
        })
        print(f"{handle} added. {i/len(remlist)*100:.2f}%")

    except Exception as e:
        print(f"💥 Exception for handle {handle}: {e}")
        failed.append(handle)

# ✅ Save everything
pd.DataFrame(details).to_csv('data/additionaldata.csv', index=False)
pd.Series(failed).to_csv('data/failed_handles.csv', index=False)

print(f"✅ Completed with {len(details)} users added and {len(failed)} failures.")
