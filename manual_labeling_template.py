import pandas as pd

data = pd.read_csv('results/data_with_tone_marks.csv')
sampled = data[['text_with_tones']].sample(100).reset_index(drop=True)
sampled['sentiment'] = ''  # empty column for manual labeling
sampled.to_csv('results/manual_labeling_template.csv', index=False)
print("Manual labeling file saved to results/manual_labeling_template.csv")