from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
    
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)  
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

                                                                                     
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm3

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route('/commits/')
def commits_graph():
    # 1. Appel à l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url).json()

    # 2. Extraction des minutes
    minutes_list = []
    for item in response:
        date_string = item["commit"]["author"]["date"]
        dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes_list.append(dt.minute)

    # 3. Compter les commits par minute
    commit_counts = {}
    for m in minutes_list:
        commit_counts[m] = commit_counts.get(m, 0) + 1

    # 4. Création du graphique
    plt.figure(figsize=(8, 4))
    plt.bar(commit_counts.keys(), commit_counts.values())
    plt.title("Nombre de commits par minute")
    plt.xlabel("Minute")
    plt.ylabel("Commits")

    # 5. Convertir en base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # 6. Affichage via template
    return render_template("commits.html", plot_url=plot_url)


if __name__ == "__main__":
    app.run(debug=True)
  
if __name__ == "__main__":
  app.run(debug=True)
