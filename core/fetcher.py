import httpx
import asyncio
from datetime import datetime

# Ücretsiz, API key gerektirmeyen kaynaklar
THREAT_FEEDS = {
    "urlhaus": "https://urlhaus-api.abuse.ch/v1/urls/recent/",
    "feodo": "https://feodotracker.abuse.ch/downloads/ipblocklist.json",
}

async def fetch_urlhaus():
    """URLhaus'dan son kötü amaçlı URL'leri çek"""
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.post(THREAT_FEEDS["urlhaus"])
            data = r.json()
            threats = []
            for item in data.get("urls", [])[:50]:  # İlk 50 kayıt
                threats.append({
                    "ip": item.get("host", "unknown"),
                    "url": item.get("url", ""),
                    "threat_type": item.get("threat", "malware"),
                    "status": item.get("url_status", "unknown"),
                    "date_added": item.get("date_added", ""),
                    "source": "URLhaus"
                })
            return threats
        except Exception as e:
            print(f"URLhaus hatası: {e}")
            return []

async def fetch_feodo():
    """Feodo Tracker'dan botnet IP'lerini çek"""
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(THREAT_FEEDS["feodo"])
            data = r.json()
            threats = []
            for item in data[:50]:
                threats.append({
                    "ip": item.get("ip_address", "unknown"),
                    "url": "",
                    "threat_type": "botnet",
                    "status": item.get("status", "unknown"),
                    "date_added": item.get("first_seen", ""),
                    "source": "Feodo"
                })
            return threats
        except Exception as e:
            print(f"Feodo hatası: {e}")
            return []

async def fetch_all_threats():
    """Tüm kaynaklardan paralel veri çek"""
    results = await asyncio.gather(
        fetch_urlhaus(),
        fetch_feodo()
    )
    all_threats = []
    for r in results:
        all_threats.extend(r)
    return all_threats

def get_threats():
    """Sync wrapper"""
    return asyncio.run(fetch_all_threats())

if __name__ == "__main__":
    threats = get_threats()
    print(f"Toplam tehdit: {len(threats)}")
    for t in threats[:3]:
        print(t)
