# Judicial Proceedings

Este proyecto es una prueba técnica para desarrollar un backend en Python que realiza scraping en una página web de consulta de procesos judiciales y expone los datos a través de una API REST usando Flask.

## Estructura del Proyecto

```plaintext
JUDICIAL_PROCEEDINGS/
│
├── src/
│   ├── controllers/
│   │   └── JudicialProceedingsScrapingController.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   └── JudicialProceedingsScrapingService.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── main.js
│   │
│   ├── json/
│   │   └── jsonschema.json
│   │
│   ├── templates/
│   │   ├── components/
│   │   │   └── base/
│   │   │       └── forms/
│   │   │           └── process_search_form.html
│   │   ├── pages/
│   │   │   ├── consult_judicial_proceedings.html
│   │   │   ├── result_search_judicial_proceedings.html
│   │   │   └── index.html
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_judicial_proceedings.py
│   │
│   ├── utils/
│   │   └── Validator.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt