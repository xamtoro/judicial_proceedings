from flask import Flask, render_template, request, jsonify
from utils.Validator import Validator as VD

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/consult-judicial-proceedings')
def consult_judicial_proceedings():
    return render_template('pages/consult_judicial_proceedings.html')

@app.post('/result-search-judicial-proceedings')
def result_search_judicial_proceedings():
    try:
        validated_data = VD.validate_data(request, "consult_judicial_proceedings")
        return render_template('pages/result_search_judicial_proceedings.html')

    except Exception as e:
        return render_template('pages/consult_judicial_proceedings.html', error = e)