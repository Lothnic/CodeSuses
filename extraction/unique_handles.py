from typing import final
import pandas as pd

base_api = "https://codeforces.com/api/"

# Authentication is not required for this project but might come in handy for others

# load_dotenv()
# key = os.getenv('ID')
# secret = os.getenv('SECRET')

df = pd.read_csv('data/contest_list.csv')
contest_list = df['id'].tolist()

handles = set()

for id in contest_list:
    try:
        data = pd.read_csv(f'data/{id}.csv')
        user_list = data['0'].tolist()

        for user in user_list:
            handles.add(user)

    except:
        pass

final_handles = pd.DataFrame(handles)
final_handles.to_csv('data/handles.csv', index=False)

    

