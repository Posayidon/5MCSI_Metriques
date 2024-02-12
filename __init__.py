from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import base64

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #verif2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

def get_commit_data():
    url = "https://api.github.com/repos/Posayidon/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()

    commit_counts = {}
    for commit in commits:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.strftime('%Y-%m-%d %H:%M')
        commit_counts[minute] = commit_counts.get(minute, 0) + 1
    
    data_for_chart = []
    for minute, count in commit_counts.items():
        data_for_chart.append([minute, count])
    
    return data_for_chart

@app.route('/commits/')
def show_commits():
    return render_template('commits.html')

@app.route('/commits/data')
def commits_data():
    data = get_commit_data()
    return jsonify(data)
  
if __name__ == "__main__":
  app.run(debug=True)
