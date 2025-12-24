from flask import Flask, render_template, request
import joblib
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load trained model
model = joblib.load("startup_funding_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    img = None

    if request.method == "POST":
        # ---------- INPUTS ----------
        amount = float(request.form["amount"])
        top_city = int(request.form["top_city"])

        # Model input (2 features only)
        data = np.array([[amount, top_city]])

        # Prediction
        pred = model.predict(data)[0]

        # Probability
        proba = model.predict_proba(data)[0]
        low_prob = round(proba[0] * 100, 2)
        high_prob = round(proba[1] * 100, 2)

        # Prediction text
        if pred == 1:
            prediction = "🚀 High Value Funding"
        else:
            prediction = "⚠️ Low Value Funding"

        # ---------- GRAPH ----------
        plt.figure(figsize=(4,3))

        labels = ["Low Value", "High Value"]
        values = [low_prob, high_prob]
        colors = ["#ff4d4d", "#00c853"]

        plt.bar(labels, values, color=colors)
        plt.ylabel("Probability (%)")
        plt.ylim(0, 100)
        plt.title("Funding Prediction Confidence")

        plt.tight_layout()

        # Convert graph to image
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    return render_template("index.html",
                           prediction=prediction,
                           img=img)

if __name__ == "__main__":
    app.run(debug=True)
