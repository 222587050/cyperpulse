from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_ai(question: str, threat_data: list) -> str:
    threat_summary = ""
    for t in threat_data[:10]:
        threat_summary += f"- IP: {t.get('ip')} | Tur: {t.get('threat_type')} | Risk: {t.get('risk_score', '?')} | Durum: {t.get('status')}\n"

    prompt = f"""
Sen bir siber guvenlik uzmanisın.
Asagida gercek zamanli tehdit verileri var:

{threat_summary}

Kullanicinin sorusu: {question}

Turkce olarak kisa ve net yanit ver.
Teknik terimleri acikla.
Aksiyon onerileri sun.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def generate_report(threat_data: list, metrics: dict) -> str:
    threat_summary = ""
    for t in threat_data[:20]:
        threat_summary += f"- IP: {t.get('ip')} | Tur: {t.get('threat_type')} | Risk: {t.get('risk_score', '?')}\n"

    prompt = f"""
Sen bir siber guvenlik analisti olarak asagidaki verileri raporla:

MODEL METRIKLERI:
- Toplam analiz: {metrics.get('total_analyzed')}
- Anomali tespit: {metrics.get('anomalies_detected')}
- Anomali orani: {metrics.get('anomaly_rate')}%
- Kritik tehdit: {metrics.get('critical')}
- Orta seviye: {metrics.get('medium')}
- Dusuk seviye: {metrics.get('low')}

EN TEHLIKELI IP'LER:
{threat_summary}

Asagidaki formatta Turkce rapor yaz:

1. YONETICI OZETI (2-3 cumle)
2. EN KRITIK TEHDITLER
3. TREND ANALIZI
4. ONERILEN AKSIYONLAR

Profesyonel ve net ol.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text