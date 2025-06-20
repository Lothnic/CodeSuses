import aiohttp
import asyncio
import pandas as pd
import os
import time
from aiohttp import ClientSession, ClientTimeout

BATCH_SIZE = 500
CONCURRENT_REQUESTS = 10
RETRIES = 3
SAVE_INTERVAL = 1
HANDLE_FILE = 'data/handles.csv'
OUTPUT_FILE = 'data/fulldata.csv'

semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
progress_file = 'data/_progress.log'

async def fetch_user_info(session: ClientSession, handles: list[str], attempt=1):
    handles_str = ';'.join(handles)
    url = f"https://codeforces.com/api/user.info?handles={handles_str}&checkHistoricHandles=false"
    try:
        async with semaphore:
            async with session.get(url, timeout=ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")
                json_data = await resp.json()
                if json_data['status'] != 'OK':
                    raise Exception(f"CF API error: {json_data['comment']}")
                return json_data['result']
    except Exception as e:
        if attempt < RETRIES:
            await asyncio.sleep(2 * attempt)
            return await fetch_user_info(session, handles, attempt + 1)
        print(f"Failed batch: {handles[:5]}... ({len(handles)} handles): {e}")
        return []

def process_user(user):
    return {
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
    }

async def process_all_batches(all_handles):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            done_until = int(f.read())
    else:
        done_until = 0

    batches = [all_handles[i:i + BATCH_SIZE] for i in range(done_until, len(all_handles), BATCH_SIZE)]
    print(f"Starting async processing of {len(batches)} batches...")

    all_records = []
    async with aiohttp.ClientSession() as session:
        for idx, batch in enumerate(batches):
            result = await fetch_user_info(session, batch)
            if result:
                all_records.extend([process_user(user) for user in result])
            if (idx + 1) % SAVE_INTERVAL == 0 or idx == len(batches) - 1:
                df_temp = pd.DataFrame(all_records)
                df_temp.to_csv(OUTPUT_FILE, index=False)
                with open(progress_file, 'w') as f:
                    f.write(str(done_until + (idx + 1) * BATCH_SIZE))
                print(f"Saved progress at batch {idx + 1}")
    return all_records

def main():
    df = pd.read_csv(HANDLE_FILE)
    handles = df['handles'].dropna().unique().tolist()
    start = time.time()
    asyncio.run(process_all_batches(handles))
    print(f"Done in {round(time.time() - start, 2)} seconds")

if __name__ == '__main__':
    main()
