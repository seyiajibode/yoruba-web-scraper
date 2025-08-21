from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = 'results/data_with_tone_marks.csv'
SAVE_FILE = 'results/labeled_sentiment.csv'

if os.path.exists(SAVE_FILE):
    labeled_df = pd.read_csv(SAVE_FILE)
    labeled_ids = set(labeled_df['id'].tolist())
else:
    labeled_df = pd.DataFrame(columns=['id', 'text_with_tones', 'sentiment'])
    labeled_ids = set()

df = pd.read_csv(DATA_FILE)
df = df.reset_index().rename(columns={'index': 'id'})

@app.route('/')
@app.route('/<int:current_id>')
def index(current_id=0):
    for idx in range(current_id, len(df)):
        if df.loc[idx, 'id'] not in labeled_ids:
            return render_template('label.html', text=df.loc[idx, 'text_with_tones'], id=df.loc[idx, 'id'], next_id=idx+1)
    return "✅ All items have been labeled. Thank you!"

@app.route('/submit', methods=['POST'])
def submit():
    text_id = int(request.form['id'])
    sentiment = request.form['sentiment']

    global labeled_df
    labeled_df = pd.concat([labeled_df, pd.DataFrame([{
        'id': text_id,
        'text_with_tones': df.loc[df['id'] == text_id, 'text_with_tones'].values[0],
        'sentiment': sentiment
    }])], ignore_index=True)

    labeled_df.to_csv(SAVE_FILE, index=False)
    return redirect(url_for('index', current_id=text_id + 1))

@app.route('/skip/<int:text_id>')
def skip(text_id):
    return redirect(url_for('index', current_id=text_id + 1))

if __name__ == '__main__':
    app.run(debug=True)