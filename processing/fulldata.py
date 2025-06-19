import requests
import pandas as pd

df = pd.read_csv('data/handles.csv')
handles = df['handles'].tolist()

for handle in handles:
    print(handle)