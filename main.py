from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def weather(station, date):

    local_station = str(station).zfill(6)
    file_route = "data_small/TG_STAID" + local_station + ".txt"
    df = pd.read_csv(file_route, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<subject>")
def dictionary(subject):
    local_value = str(subject).upper()
    return {"definition": local_value,
            "word": subject}

if __name__ == "__main__":
    app.run(debug=True, port=5000)