import pandas
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def weather(station, date):
    local_station = str(station).zfill(6)
    file_route = "data_small/TG_STAID" + local_station + ".txt"
    df = pd.read_csv(file_route, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    local_station = str(station).zfill(6)
    file_route = "data_small/TG_STAID" + local_station + ".txt"
    df = pd.read_csv(file_route, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

@app.route("/api/v1/<station>")
def station_overall(station):
    local_station = str(station).zfill(6)
    file_route = "data_small/TG_STAID" + local_station + ".txt"
    df = pd.read_csv(file_route, skiprows=20, parse_dates=["    DATE"])

    return df.to_dict(orient="records")


#Exercise with the dictionary example
"""  
@app.route("/api/v1/<subject>")
def dictionary(subject):
    df = pandas.read_csv("dictionary.csv")
    definition = df.loc[df["word"] == subject]["definition"].squeeze()
    return {"definition": definition,
            "word": subject}
"""
if __name__ == "__main__":
    app.run(debug=True, port=5000)
