# 🛡️ CyberPulse AI

> AI-powered cyber threat intelligence dashboard with ML anomaly detection

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-orange)
![AI](https://img.shields.io/badge/AI-Gemini%202.0-red)

## 🎯 Proje Hakkında

CyberPulse AI, gerçek zamanlı siber tehdit verilerini toplayıp makine öğrenmesi ile analiz eden ve sonuçları web dashboard üzerinden sunan bir tehdit istihbarat sistemidir.

## ⚡ Özellikler

- 🔍 **Gerçek Zamanlı Tehdit Tarama** — Feodo Tracker ve URLhaus'dan canlı botnet/malware verisi
- 🧠 **ML Anomali Tespiti** — Isolation Forest ile bilinmeyen tehditleri otomatik tespit
- 📊 **Risk Skorlama** — Her IP için 0-100 arası dinamik risk skoru
- 🤖 **AI Asistan** — Gemini 2.0 ile tehditler hakkında doğal dil sorgusu
- 📄 **Otomatik Rapor** — Tek tıkla profesyonel tehdit raporu üretimi
- 📈 **Analitik Dashboard** — Tehdit trendi ve dağılım grafikleri

## 🏗️ Mimari
Ham Veri (API)
↓
EDA & Temizleme (Pandas)
↓
Isolation Forest (Scikit-learn)
↓
Risk Skorlama
↓
Web Dashboard (Flask + Chart.js)
↓
AI Analizi (Gemini 2.0)

## 🛠️ Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python, Flask |
| Veri Analizi | Pandas, NumPy |
| Makine Öğrenmesi | Scikit-learn (Isolation Forest) |
| AI | Google Gemini 2.0 |
| Frontend | HTML, CSS, Chart.js |
| Veritabanı | SQLite |
| Veri Kaynakları | Feodo Tracker, URLhaus |

## 🚀 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/222587050/cyberpulse.git
cd cyberpulse

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyası oluştur
echo "GEMINI_API_KEY=your_key_here" > .env

# Çalıştır
python app.py
```

Tarayıcıda `http://localhost:5000` adresini aç.

## 📊 Model Metrikleri

- **Algoritma:** Isolation Forest
- **Contamination:** %10
- **Özellikler:** is_active, is_botnet, is_url_threat, source_score, ip_first_octet
- **Sliding Window:** Son 1000 kayıt

## 📸 Ekran Görüntüsü

> Dashboard ekran görüntüsü eklenecek

## 👤 Geliştirici

**Mehmet Onal** — Bursa Uludağ Üniversitesi