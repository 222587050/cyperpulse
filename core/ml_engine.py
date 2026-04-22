import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "is_url_threat",
    "is_botnet",
    "is_active",
    "source_score",
    "ip_first_octet"
]

def train_isolation_forest(df):
    if df.empty or len(df) < 3:
        return None, None
    X = df[FEATURES].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X_scaled)
    return model, scaler

def predict_anomalies(df, model, scaler):
    if model is None or df.empty:
        return df
    X = df[FEATURES].fillna(0)
    X_scaled = scaler.transform(X)
    df["anomaly_score"] = model.decision_function(X_scaled)
    df["is_anomaly"] = model.predict(X_scaled)
    df["is_anomaly"] = df["is_anomaly"].apply(lambda x: 1 if x == -1 else 0)
    return df

def calculate_risk_score(df):
    if df.empty:
        return df
    df["risk_score"] = 0
    df["risk_score"] += df["is_active"] * 30
    df["risk_score"] += df["is_botnet"] * 25
    df["risk_score"] += df["is_url_threat"] * 25
    df["risk_score"] += df.get("is_anomaly", 0) * 20
    df["risk_score"] = df["risk_score"].clip(0, 100)

    def risk_label(score):
        if score >= 70:
            return "KRITIK"
        elif score >= 40:
            return "ORTA"
        else:
            return "DUSUK"

    df["risk_label"] = df["risk_score"].apply(risk_label)
    return df

def get_model_metrics(df):
    if df.empty or "is_anomaly" not in df.columns:
        return {}
    total = len(df)
    anomalies = int(df["is_anomaly"].sum())
    return {
        "total_analyzed": total,
        "anomalies_detected": anomalies,
        "anomaly_rate": round(anomalies / total * 100, 2),
        "critical": int((df["risk_score"] >= 70).sum()),
        "medium": int(((df["risk_score"] >= 40) & (df["risk_score"] < 70)).sum()),
        "low": int((df["risk_score"] < 40).sum()),
        "model": "Isolation Forest"
    }

if __name__ == "__main__":
    from fetcher import get_threats
    from eda import clean_threats
    print("Veri cekiliyor...")
    threats = get_threats()
    df = clean_threats(threats)
    print("Model egitiliyor...")
    model, scaler = train_isolation_forest(df)
    df = predict_anomalies(df, model, scaler)
    df = calculate_risk_score(df)
    print(get_model_metrics(df))
    print(df[["ip", "threat_type", "risk_score", "risk_label"]].head(5))