from core.fetcher import get_threats
from core.eda import clean_threats, get_stats
from core.ml_engine import train_isolation_forest, predict_anomalies, calculate_risk_score, get_model_metrics

threats = get_threats()
df = clean_threats(threats)
model, scaler = train_isolation_forest(df)
df = predict_anomalies(df, model, scaler)
df = calculate_risk_score(df)
print("Toplam:", len(df))
print("Metrikler:", get_model_metrics(df))
