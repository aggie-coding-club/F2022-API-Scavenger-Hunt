import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Use a service account
cred = credentials.Certificate('f2021-api-scavenger-hunt-firebase-adminsdk-srfna-5cc4ecb304.json')
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
        return 'Welcome! Create a POST request on the same URL with the full forms of the acronym "acc" via the following JSON object {"acc": "your_answer_here"}'

# First Task
@app.route('/numofficers', methods=['POST'])
def numOfficers():
    if request.method == 'POST':

        json = request.get_json()

        if 'num_officers' in json:
            numOfficers = json['num_officers']
            if type(numOfficers) is int:
                numOfficers = str(numOfficers)
            if numOfficers.isnumeric() and int(numOfficers) == 8:
                return "You are on a roll! For the next question, make a GET request to https://acc-api-scavenger-hunt.herokuapp.com//blackandwhite/<your_answer_here> with the first name of the only officer that has a black and white photo. Go to https://aggiecodingclub.com to find out!"
            else:
                return "Hmmm... Didn't get the number quite right. Try again!"
        else:
            return "Not quite! Make sure your key is num_officers."


@app.route('/blackandwhite/<firstname>', methods=['GET'])
def firstname(firstname):
    if request.method == 'GET':
        if firstname.lower() == 'hannah':
            return 'You are an expert! Where did Dakshika "Empower students to use new technologies"? Gather the company name and send a POST request to https://acc-api-scavenger-hunt.herokuapp.com/empower with the JSON object {"company": "your_answer_here"}.'
        else:
            return "Not quite! Make sure you spelled her first name right! Hint: She was one of ACC's past Presidents!"


@app.route('/empower', methods=['POST'])
def empoweringStudents():
    if request.method == 'POST':

        json = request.get_json()

        if json is None:
            return "You didn't provide a JSON body. Try again!"
        if 'company' in json:
            if json['company'].lower() == 'microsoft':
                return "Sweet! We talked about this one at our first meeting and it turned a lot of heads! What was Anthony's favorite pizza topping? Make a GET request to https://acc-api-scavenger-hunt.herokuapp.com/pizza/topping/<your_answer_here>"
            else:
                return "Hmmm... Didn't get the company name quite right. Try again!"
        else:
            return "Not quite! A Google search may be helpful here."


@app.route('/pizza/toppings/<topping>', methods=['GET'])
def pizza(topping):
    if request.method == 'GET':
        if topping.lower() == 'strawberries' or topping.lower() == 'strawberry':
            return 'What is going on!?!? You are a genius! Ok this one is the last trivia question, we promise! What is the height of the photo on our landing page? Just specify the number of pixels. Make a POST request to https://acc-api-scavenger-hunt.herokuapp.com/static/images/acc-website-graphics with the JSON object {"height": "your_answer_here"}.'
        else:
            return "Not quite! Check out the sldies from our first meeting. I have a feeling it's there."

@app.route('/static/images/acc-website-graphics', methods=['POST'])
def finalStretch():
    if request.method == 'POST':

        json = request.get_json()

        if 'height' in json:
            height = json['height']
            if type(height) is int:
                height = str(height)
            if height.isnumeric() and int(height) == 400:
                return 'CONGRATULATIONS! Send a POST request to https://acc-api-scavenger-hunt.herokuapp.com/leaderboard with the JSON body {"name": "your_name_here"}.'
            else:
                return "Hmmm... Didn't get the height quite right. Try again!"
        else:
            return "Not quite! Make sure you send it as 'height' and not 'max_height'. Hint: You may need to INSPECT it closer if you want to count all the pixels."

@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    if request.method == 'POST':
        json = request.get_json()

        if 'name' in json:
            name = json['name']

            doc_ref = db.collection(u'hall_of_fame')
            data = {
                u'name': name
            }

            doc_ref.add(data)

            return "Check out the leaderboard! You should be on it now."
        else:
            return "Not quite! Make sure your key is name."

if __name__ == '__main__':
    app.run(port=8080)