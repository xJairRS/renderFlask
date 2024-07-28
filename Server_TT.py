# Flask
from flask import Flask,jsonify, render_template, request
# Data manipulation
import pandas as pd
# Matrices manipulation
import numpy as np
# Script logging
import logging
# ML model
import joblib
# JSON manipulation
import json
# Utilities
import sys
import os
from flask_cors import CORS
import requests  # Importar requests para enviar datos a Express

# Current directory
current_dir = os.path.dirname(__file__)

# Flask app
app = Flask(__name__, static_folder = 'static', template_folder = 'template')
# O para permitir de todos los orígenes (no recomendado para producción)
CORS(app, resources={r"/prediction*": {"origins": "https://api-agrosabio.onrender.com"}})
# Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Function
def ValuePredictor(data = pd.DataFrame):
	# Model name
	model_name = 'model_TT_RFC.pkl'
	# Directory where the model is stored
	model_dir = os.path.join(current_dir, model_name)
	# Load the model
	loaded_model = joblib.load(open(model_dir, 'rb'))
	# Predict the data
	result = loaded_model.predict(data)
	return result[0]

# Función para enviar datos a la API de Express
def send_data_to_express(data):
    url = "https://api-agrosabio.onrender.com/api/store"  
 
    response = requests.post(url, json=data)  
    return response.json()  

@app.errorhandler(500)
def handle_500(error):
    return jsonify({"error": str(error), "status": "error"}), 500


@app.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not found", "status": "error"}), 404

# Home page
@app.route('/')
def home():
	return render_template('index.html')

# Prediction page
@app.route('/prediction', methods=['POST'])
def predict():
    try:
        # Get the data from form
        nitrogen = float(request.form.get('Nitrogen', 0))
        potassium = float(request.form.get('Potassium', 0))
        humidity = float(request.form.get('Humidity', 0))
        phosphorus = float(request.form.get('Phosphorus', 0))
        pH_Value = float(request.form.get('pH_Value', 0))
        temperature = float(request.form.get('Temperature', 0))

        # Additional code remains the same

        data = {    
            'Nitrogen': nitrogen,
            'Potassium': potassium,
            'Humidity': humidity,
            'Phosphorus': phosphorus,
            'pH_Value': pH_Value,
            'Temperature': temperature
        }

        # Load columns schema
        schema_name = 'columns_set.json'
        schema_dir = os.path.join(current_dir, schema_name)
        with open(schema_dir, 'r') as f:
            cols = json.loads(f.read())['data_columns']

        # Prepare data for prediction
        df = pd.DataFrame([data], columns=cols)

        # Create a prediction
        result = ValuePredictor(data=df)
        
         # Enviar datos a la API de Express
        express_response = send_data_to_express(data)

        # Determine the output
        if int(result) == 1:
            prediction = '¡Es un muy buen suelo para sembrar!'
            good_soil = True
        else:
            prediction = '¡No es un suelo apto para sembrar caña, pero se puede mejorar!'
            good_soil = False

        response = {
            'status': 'success',
            'data': data,
            'prediction': prediction,
            'good_soil': good_soil,
            'express_response': express_response
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }

    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)