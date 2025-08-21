import pandas as pd
import re

data = pd.read_csv('yoruba_text_data.csv')

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'http\S+', '', str(text))
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

data['cleaned_text'] = data['text'].apply(clean_text)
data.to_csv('results/cleaned_data.csv', index=False)
print("Cleaning done! Check results/cleaned_data.csv")