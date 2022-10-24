import requests
import firebase_admin
import datetime
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, request, redirect
from firebase_admin.firestore import SERVER_TIMESTAMP
app = Flask(__name__)

# Use a service account
cred = credentials.Certificate('api-scavenger-hunt-firebase-adminsdk-khivo-5707909885.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# Intro task
@app.route('/', methods=['POST', 'GET'])
def home():
    # POST
    if request.method == 'POST':

        json = request.get_json()
        if json is None:
            return "You didn't provide a JSON body. Try again!"
        elif 'acc' in json:
            if json['acc'].lower() == "aggie coding club":
                return "That's Correct! For the next question, make a POST request to https://acc-api-scavenger-hunt.herokuapp.com//numofficers with a JSON object payload of key “num_officers” and the value as an integer number as your answer to how many officers ACC has. Go to https://aggiecodingclub.com to find out!"
            else:
                return "Hmmm... I don't think you spelled the acronym correctly. Try again!"
        else:
            return 'Not quite! Make sure you have no extra spaces. The values for each acronymn be the full form. POST a JSON object {"acc": "your_answer_here"} on the same url'
    else:
        return 'Welcome!!!!!! Create a POST request on the same URL. Include a JSON object with ACC\'s full name. JSON object {"acc": "your_answer_here"}'

# First Task
@app.route('/numofficers', methods=['POST'])
def numOfficers():
    if request.method == 'POST':

        json = request.get_json()

        if 'num_officers' in json:
            numOfficers = json['num_officers']
            if type(numOfficers) is int:
                numOfficers = str(numOfficers)
            if numOfficers.isnumeric() and int(numOfficers) == 7:
                return "STUNNING! \n. Next question: When is the deadline for the ACC Discord Bot Competition? Make a GET request to https://acc-api-scavenger-hunt.herokuapp.com//discord/deadline/MM-DD-YYYY" 
            else:
                return "Hmmm... Didn't get the number quite right. Try again!"
        else:
            return "Not quite! Make sure your key is num_officers."

@app.route('/discord/deadline/<deadline>', methods=['GET'])
def discordDeadline(deadline):
    if request.method == 'GET':
        if( deadline == '11-14-2022'):
            return "You are on a roll! \n. Next question: Where was Casey? Make a GET request to https://acc-api-scavenger-hunt.herokuapp.com//casey_travels/<YOUR_CITY_ANSWER_HERE>"
        elif (deadline == '11-21-2022'):
            return "hmmm, this is the when winners are announced, not quite the deadline"
        else:
            return "Not yet, make sure to look up the deadline on the discord!"
    else:
        return "Hmmmm, make sure your key is \'deadline\' in your json object"

@app.route('/casey_travels/<location>', methods=['GET'])
def location(location):
    if request.method == 'GET':
        if location.lower() == 'florence':
            return 'You are an expert! \n What is the oldest acc code? Gather the name and send a POST request to https://acc-api-scavenger-hunt.herokuapp.com/ancient with the JSON object {"code": "your_answer_here"}.'
        if location.lower() == 'college station' or location.lower() == 'cstat':
            return "Not quite! Remember, where WAS casey"
        else:
            return "Hmmmmm, find out where Casey has been in the past."


@app.route('/ancient', methods=['POST'])
def oldestCode():
    if request.method == 'POST':

        json = request.get_json()

        if json is None:
            return "You didn't provide a JSON body. Try again!"
        if 'code' in json:
            if json['code'].lower() == 'liftr':
                return "What is going on?!?!? You're a genius! \n Ready for the last one? \n Who \'... specializes … work into the field. Personal … traveling … good food … gaming.'\' Make a GET request to https://acc-api-scavenger-hunt.herokuapp.com/blank/person/<your_answer_here>"
            else:
                return "Hmmm... Didn't get the repo name quite right. Try again!"
        else:
            return "Not quite! A github search may be helpful here."


@app.route('/blank/person/<name>', methods=['GET'])
def person(name):
    if request.method == 'GET':
        if name.lower() == 'feras' or name.lower() == 'khemakhem':
            return 'CONGRATULATIONS! Send a POST request to https://acc-api-scavenger-hunt.herokuapp.com/leaderboard with the JSON body {"name": "your_name_here"}.'
        else:
            return "Not quite! Remember this whole scavenger hunt is ACC themed!"

@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    if request.method == 'POST':
        json = request.get_json()

        if 'name' in json:
            name = json['name']

            doc_ref = db.collection(u'hall_of_fame')
            data = {
                u'name': name,
                'created': SERVER_TIMESTAMP,
            }

            doc_ref.add(data)

            return "Check out the leaderboard! You should be on it now."
        else:
            return "Not quite! Make sure your key is name."

if __name__ == '__main__':
    app.run(port=8080)