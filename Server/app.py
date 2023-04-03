import urllib.request
from flask import Flask, jsonify
from flask_cors import CORS
import schedule
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500, https://umairsyed613.github.io"}})

@app.route('/gettodayprices', methods=['GET'])
def gettodayprices():
    with open('data.json', 'rb') as openfile:
        data = json.load(openfile)
    return jsonify(data)

@app.route('/run_job', methods=['GET'])
def run_job():
    daily_job()
    return "Daily job ran successfully"

def daily_job():
    url = 'https://prod-publicservices.azurewebsites.net/api/spotprices/ts/auto'
    response = urllib.request.urlopen(url)
    data = response.read()
    with open("data.json", "wb") as outfile:
        outfile.write(data)
    print("Running daily job...")

# Schedule the daily job to run every day at midnight
schedule.every().day.at("08:00").do(daily_job)

if __name__ == '__main__':
    schedule.every().day.at("08:00").do(daily_job)
    app.run()
