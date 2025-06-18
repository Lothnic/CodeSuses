import pandas as pd

df = pd.read_csv('enhanced_filtered_users.csv')

print(df['cheating'].value_counts())
print(df['cheating'].sum())