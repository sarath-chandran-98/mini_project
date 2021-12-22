from flask import Flask,render_template

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
text ="Naruto is a Japanese manga series written and illustrated by Masashi Kishimoto. It tells the story of Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village."

doc = nlp(text)
token = [token.text for token in doc]
punctuation = punctuation + '\n'

word_frequency = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1
max_frequency = max(word_frequency.values())

for word in word_frequency.keys():
    word_frequency[word] = word_frequency[word]/max_frequency

sentence_tokens = [sent for sent in doc.sents]
sentence_scores = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequency.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_frequency[word.text.lower()]
            else:
                sentence_scores[sent] += word_frequency[word.text.lower()]

select_length = int(len(sentence_scores)*0.5)
summary = nlargest(select_length,sentence_scores,key = sentence_scores.get )
final_summary = [word.text for word in summary]
summary =  ' '.join(final_summary)


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("sum.html",result=summary)



if __name__ == '__main__':
    app.run()



