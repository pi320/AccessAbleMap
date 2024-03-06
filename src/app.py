from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from src.config.config import Config
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # Make sure to set this in your environment variables
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# Lookup places
@app.route('/lookup_places', methods=['GET'])
def lookup_places():
    input_text = request.args.get('input')
    if not input_text:
        return jsonify({'error': 'Missing input parameter'}), 400

    params = {
        'input': input_text,
        'inputtype': 'textquery',
        'fields': 'formatted_address,name,geometry',
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(PLACES_API_URL, params=params)
    if response.status_code == 200:
        return jsonify(response.json()['candidates'])
    else:
        return jsonify({'error': 'Failed to fetch places'}), response.status_code


# Get database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

# Get saved places from database
def get_saved_places(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places WHERE user_id = %s', (user_id,))
    places = cur.fetchall()
    cur.close()
    conn.close()
    return places

# Return saved places to user
@app.route('/saved_places', methods=['GET'])
def saved_places():
    user_id = request.args.get('user_id')  # Assuming user_id is passed as a query parameter
    places = get_saved_places(user_id)
    return jsonify(places)

if __name__ == '__main__':
    app.run(debug=True)