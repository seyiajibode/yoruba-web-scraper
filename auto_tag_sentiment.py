import pandas as pd

positive_words = {'dára', 'tóbi', 'wá', 'fẹ́ràn', 'yẹ', 'ayọ̀', 'aláyọ̀', 'réré', 'gbadun', 'dun'}
negative_words = {'bùrú', 'kò', 'fẹ̀sùn', 'bínú', 'róyìn', 'ìbànújẹ', 'jìyà', 'ṣòro', 'fojú'}

def weak_sentiment_tag(text):
    words = set(text.lower().split())
    pos_score = len(words & positive_words)
    neg_score = len(words & negative_words)
    if pos_score > neg_score:
        return 'positive'
    elif neg_score > pos_score:
        return 'negative'
    elif pos_score == 0 and neg_score == 0:
        return 'neutral'
    else:
        return 'neutral'

data = pd.read_csv('results/data_with_tone_marks.csv')
data['weak_sentiment'] = data['text_with_tones'].apply(weak_sentiment_tag)
data.to_csv('results/auto_tagged_sentiment.csv', index=False)
print("Auto sentiment tagging complete! Check results/auto_tagged_sentiment.csv")