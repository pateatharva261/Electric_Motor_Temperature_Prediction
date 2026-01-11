from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("model.pkl")  # Replace with your actual model path

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            features = [
                float(request.form["u_q"]),
                float(request.form["coolant"]),
                float(request.form["u_d"]),
                float(request.form["motor_speed"]),
                float(request.form["i_d"]),
                float(request.form["i_q"]),
                float(request.form["ambient"]),
                float(request.form["profile_id"])
            ]

            pred = model.predict([features])[0]  # Assuming model returns array
            prediction = {
                "stator_winding": round(pred[3], 2),
                "stator_yoke": round(pred[1], 2),
                "stator_tooth": round(pred[2], 2),
                "pm": round(pred[0], 2)
            }
        except Exception as e:
            prediction = {"error": str(e)}

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
