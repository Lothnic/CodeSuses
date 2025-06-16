from dotenv import load_dotenv
import pandas as pd
import os
import requests
import csv
import time

base_api = "https://codeforces.com/api/"

# Authentication is not required for this project but might come in handy for others

# load_dotenv()
# key = os.getenv('ID')
# secret = os.getenv('SECRET')

df = pd.read_csv('data/contest_list.csv')
contest_list = df['id'].tolist()

for id in contest_list:
    handles = set()
    contest_standing = requests.get(f'{base_api}contest.standings?contestId={id}')
    for row in contest_standing.json()['result']['rows']:
        for member in row['party']['members']:
            handles.add(member['handle'])
    file = pd.DataFrame(handles)
    file.to_csv(f'data/{id}.csv', index=False) 

