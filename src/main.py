from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token
from controllers.JudicialProceedingsScrapingController import JudicialProceedingsScrapingController as JSPC
from utils.Validator import Validator
from datetime import timedelta
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_SECRET_KEY"] = getenv("SECRET")
app.config["SECRET_KEY"] = getenv("SECRET")
jwt = JWTManager(app)

PAGES_PATH = getenv("PAGES_PATH")

@app.get('/')
def index():
    return render_template('index.html')

"""
Note: this is a simple login api, it will simply serve to generate the
access token to authenticate the main api :D.
"""
#Api for login and return access token
@app.post("/login")
def login():
    try:
        validated_data = Validator.validate_data(request, "login")

        #Test credentials
        AUTHORIZED_MAIL = getenv("EMAIL")
        AUTHORIZED_PASSWORD = getenv("PASSWORD")

        if (validated_data.get("email") == AUTHORIZED_MAIL) and \
           (validated_data.get("password") == AUTHORIZED_PASSWORD):

            access_token = create_access_token(identity=validated_data)
            refresh_token = create_refresh_token(identity=validated_data)

            return jsonify(response={"access_token": access_token, "refresh_token": refresh_token})

        else:
            raise Exception("Credenciales inválidas")

    except Exception as e:
        return jsonify(message=str(e)), 500


@app.get('/consult-judicial-proceedings')
def consult_judicial_proceedings():
    try:
        return render_template(f'{PAGES_PATH}consult_judicial_proceedings.html')
    except Exception as e:
        return jsonify(message = str(e)), 500

@app.post('/court-records-found')
def court_records_found():
    try:
        validated_data = Validator.validate_data(request, "consult_judicial_proceedings")

        controller = JSPC()
        records = controller.fill_form_and_submmit(validated_data)

        return render_template(f'{PAGES_PATH}result_search_judicial_proceedings.html', records=records)

    except Exception as e:
        flash(Validator.validate_type_error(e))
        return redirect('consult-judicial-proceedings')

@app.post('/result-search-judicial-proceedings')
@jwt_required()
def result_search_judicial_proceedings():
    try:
        validated_data = Validator.validate_data(request, "consult_judicial_proceedings")

        controller = JSPC()
        records = controller.fill_form_and_submmit(validated_data)
        print(records)
        return jsonify({"response": records})

    except Exception as e:
        return jsonify(message = str(e)), 500