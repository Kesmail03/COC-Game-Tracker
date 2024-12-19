"""
A clash of clans tracker flask app.
"""
from flask import Flask, render_template, request
import os
import requests
from google.cloud import datastore
from gbmodel import model
from flask.views import MethodView
from dotenv import load_dotenv

#load the .env file
load_dotenv()

app = Flask(__name__)       # our Flask app

#Setting the API Key
API_KEY = os.getenv("COC_API_KEY")
BASE_URL = "https://api.clashofclans.com/v1"

#Error handling 
if not API_KEY:
    raise RuntimeError("COC_API_KEY environment variable is not set")

#Initializing the datastore client and model
datastore_client = datastore.Client()
datastore_model = model()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/village', methods=['GET', 'POST'])
def village():
    #handling getting and rendering data
    #initializing the data members
    player_data = None
    troops = []
    heroes = []
    pets = []
    error = None

    player_tag = "%232PJG98CGV"


    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/players/{hard_coded_player_tag}"

    try:
        # Fetch data from the Clash of Clans API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            player_data = response.json()
            try:
                troops, heroes, pets = parse_troops_heroes_pets(player_data)
            except KeyError as e:
                error = f"Missing data field: {e}"
        else:
            error = f"Error fetching data: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        error = f"Request failed: {e}"

    return render_template(
        "village.html",
        player_data=player_data,
        troops=troops,
        heroes=heroes,
        pets=pets,
        error=error
    )
def parse_troops_heroes_pets(player_data):
    #parses the troops, heroes and equipment so I can get the info from the API
    troops = [t for t in player_data.get("troops", []) if t["village"] == "home"]
    heroes = [h for h in player_data.get("heroes", []) if h["village"] == "home"]
    pets = player_data.get("pets", [])
    return troops, heroes, pets

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
