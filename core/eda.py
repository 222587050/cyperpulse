import pandas as pd
import numpy as np
from datetime import datetime

def clean_threats(threats: list) -> pd.DataFrame:
    """Ham tehditleri temizle ve özellik çıkar"""
    
    if not threats:
        return pd.DataFrame()
    
    df = pd.DataFrame(threats)
    
    # 1. Eksik değerleri doldur
    df["ip"] = df["ip"].fillna("unknown")
    df["threat_type"] = df["threat_type"].fillna("unknown")
    df["status"] = df["status"].fillna("unknown")
    df["date_added"] = df["date_added"].fillna("")
    df["source"] = df["source"].fillna("unknown")

    # 2. Tekrar eden IP'leri kaldır
    df = df.drop_duplicates(subset=["ip"])

    # 3. Yeni özellikler üret (Feature Engineering)
    df["is_url_threat"] = df["threat_type"].apply(
        lambda x: 1 if x in ["malware", "phishing", "spam"] else 0
    )
    df["is_botnet"] = df["threat_type"].apply(
        lambda x: 1 if x == "botnet" else 0
    )
    df["is_active"] = df["status"].apply(
        lambda x: 1 if x == "online" else 0
    )
    df["source_score"] = df["source"].apply(
        lambda x: 2 if x == "URLhaus" else 1
    )

    # 4. IP oktet özellikleri çıkar
    def ip_first_octet(ip):
        try:
            return int(ip.split(".")[0])
        except:
            return 0

    df["ip_first_octet"] = df["ip"].apply(ip_first_octet)

    # 5. Sliding window — son 1000 kayıt
    MAX_ROWS = 1000
    if len(df) > MAX_ROWS:
        df = df.tail(MAX_ROWS).reset_index(drop=True)

    return df

def get_stats(df: pd.DataFrame) -> dict:
    """Dashboard için istatistik üret"""
    if df.empty:
        return {}
    return {
        "total": len(df),
        "active": int(df["is_active"].sum()),
        "botnet": int(df["is_botnet"].sum()),
        "malware": int(df["is_url_threat"].sum()),
        "sources": df["source"].value_counts().to_dict(),
        "threat_types": df["threat_type"].value_counts().to_dict()
    }

if __name__ == "__main__":
    from fetcher import get_threats
    threats = get_threats()
    df = clean_threats(threats)
    print(df.head())
    print("\n📊 İstatistikler:")
    print(get_stats(df))
