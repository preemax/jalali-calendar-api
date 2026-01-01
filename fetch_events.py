import requests
from bs4 import BeautifulSoup
import json
import datetime

def get_events():
    # در نسخه نهایی، اینجا کدی می‌نویسیم که از Time.ir داده بگیرد
    # فعلاً برای تست، یک ساختار نمونه می‌سازیم
    data = {
        "year": 1404,
        "month": 10,
        "events": [
            {"d": 1, "t": "Christian New Year", "h": True},
            {"d": 11, "t": "Birthday of Imam Ali", "h": True},
            {"d": 19, "t": "Firefighting Day", "h": False},
            {"d": 30, "t": "Plasco Incident Anniversary", "h": False}
        ]
    }
    
    with open('10.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_events()
