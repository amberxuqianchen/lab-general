from clean_text import clean_text
import pandas as pd

df = pd.read_csv('psych_news.csv')
df['cleaned_text'] = df['text'].apply(clean_text)
print(df['cleaned_text'].head())