from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from core.fetcher import get_threats
from core.eda import clean_threats, get_stats
from core.ml_engine import train_isolation_forest, predict_anomalies, calculate_risk_score, get_model_metrics
from ai.chat import ask_ai, generate_report
import os

load_dotenv()

app = Flask(__name__)

# Global state
threat_cache = []
df_cache = None
model_cache = None
scaler_cache = None

def refresh_data():
    global threat_cache, df_cache, model_cache, scaler_cache
    threats = get_threats()
    df = clean_threats(threats)
    model, scaler = train_isolation_forest(df)
    df = predict_anomalies(df, model, scaler)
    df = calculate_risk_score(df)
    threat_cache = df.to_dict(orient="records")
    df_cache = df
    model_cache = model
    scaler_cache = scaler

@app.route("/")
def index():
    refresh_data()
    return render_template("dashboard.html")

@app.route("/api/threats")
def get_threat_data():
    threats = sorted(threat_cache, key=lambda x: x.get("risk_score", 0), reverse=True)
    metrics = get_model_metrics(df_cache)
    metrics["total_analyzed"] = len(threat_cache)
    return jsonify({
        "threats": threats[:50],
        "stats": get_stats(df_cache),
        "metrics": metrics
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Soru bos"}), 400
    response = ask_ai(question, threat_cache)
    return jsonify({"response": response})

@app.route("/api/report", methods=["POST"])
def report():
    metrics = get_model_metrics(df_cache)
    text = generate_report(threat_cache, metrics)
    return jsonify({"report": text})

@app.route("/api/refresh")
def refresh():
    refresh_data()
    return jsonify({"status": "ok", "total": len(threat_cache)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)