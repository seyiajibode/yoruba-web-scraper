import pandas as pd

english_words = {'the', 'and', 'is', 'are', 'was', 'have', 'this', 'that', 'you', 'me', 'we', 'they', 'good', 'bad', 'very', 'like', 'love'}
yoruba_words = {'ni', 'ti', 'si', 'ko', 'mo', 'ki', 'se', 'ba', 'wa', 'lo', 'won', 'awa', 'ninu', 'lati', 'ati', 'fun', 'ile', 'omi'}

def detect_language_type(text):
    if not isinstance(text, str) or not text.strip():
        return 'empty'
    words = text.split()
    if len(words) == 0:
        return 'empty'
    english_count = sum(1 for word in words if word in english_words)
    yoruba_count = sum(1 for word in words if word in yoruba_words)
    english_percent = english_count / len(words)
    yoruba_percent = yoruba_count / len(words)
    if english_percent > 0.3:
        return 'mostly_english'
    elif yoruba_percent > 0.3:
        return 'mostly_yoruba'
    elif english_percent > 0.1 and yoruba_percent > 0.1:
        return 'mixed_languages'
    else:
        return 'unclear'

data = pd.read_csv('results/cleaned_data.csv')
data = data.dropna(subset=['cleaned_text']).copy()
data['language_type'] = data['cleaned_text'].apply(detect_language_type)
data.to_csv('results/data_with_language_info.csv', index=False)

for lang_type in data['language_type'].unique():
    subset = data[data['language_type'] == lang_type]
    if len(subset) > 0:
        subset.to_csv(f'results/{lang_type}_texts.csv', index=False)
        print(f"Saved {len(subset)} {lang_type} texts")

print("Language detection done!")