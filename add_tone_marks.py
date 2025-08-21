import pandas as pd

tone_marks = {
    'mo': 'mo', 'o': 'ó', 'ni': 'ní', 'ti': 'tí', 'si': 'sí', 'ki': 'kí', 'lo': 'lọ', 'wa': 'wá',
    'je': 'jẹ', 'so': 'sọ', 'ko': 'kọ́', 'ri': 'rí', 'se': 'ṣe', 'wi': 'wí', 'dara': 'dára',
    'tobi': 'tóbi', 'kere': 'kéré', 'pupo': 'púpọ̀', 'omo': 'ọmọ', 'oko': 'ọkọ', 'ile': 'ilé',
    'owo': 'owó', 'ori': 'orí', 'omi': 'omi', 'aso': 'aṣọ', 'oni': 'òní', 'ana': 'àná', 'ola': 'ọ̀la'
}

def add_tone_marks(text):
    words = text.split()
    fixed_words = []
    for word in words:
        clean_word = word.strip(".,!?")
        if clean_word in tone_marks:
            fixed_word = word.replace(clean_word, tone_marks[clean_word])
            fixed_words.append(fixed_word)
        else:
            fixed_words.append(word)
    return ' '.join(fixed_words)

def count_tone_marks(text):
    tone_chars = 'áàâäéèêëẹ́ẹ̀íìîïóòôöọ́ọ̀úùûüńǹṣṣ́ṣ̀'
    return sum(1 for char in text if char in tone_chars)

data = pd.read_csv('results/data_with_language_info.csv')
data['text_with_tones'] = data['cleaned_text'].apply(add_tone_marks)
data['tone_mark_count'] = data['text_with_tones'].apply(count_tone_marks)
data.to_csv('results/data_with_tone_marks.csv', index=False)
print("Tone marks added and saved to results/data_with_tone_marks.csv")