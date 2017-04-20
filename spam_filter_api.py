#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pandas as pd
import nltk
nltk.data.path.append('./nltk_data')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from sklearn.externals import joblib

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/spam_filter', methods=['POST'])
def spam_filter():

    # Sms
    message = request.form['sms']

    # Pré-processamento
    filtered_message = preprocess(message)

    # Classificação
    pred = clf.predict([filtered_message])
    if pred == 1:
        resp = 'spam'
    elif pred == 0:
        resp = 'ham'

    return jsonify(classification=resp)


# Função de pré processamento
def preprocess(string):
    tokens = word_tokenize(string.decode('utf-8'))
    low_tokens = [token.lower() for token in tokens \
                    if token not in stopwords.words('english')]
    string = " ".join(low_tokens)
    string = re.sub(r'\d{1,}','NUM',string)
    string = re.sub(r'[^a-z\s]','',string)
    return string

if __name__ == '__main__':
    # Carregar modelo
    clf = joblib.load('spam_filter.pkl')
    # Usar porta 5005
    app.run(debug=False, port=5005)
