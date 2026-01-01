import requests
import json
import time
import os

def translate_to_english(text):
    try:
        # استفاده از API رایگان گوگل برای ترجمه
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fa&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        return r.json()[0][0][0]
    except:
        return text

def fetch_month(year, month):
    events_english = []
    print(f"Fetching Month {month}...")
    
    # دریافت دیتای کل ماه از API فارسی
    api_url = f"https://holidayapi.ir/jalali/{year}/{month}"
    try:
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # ساختار API برای کل ماه ممکن است لیستی از روزها باشد
            for day_data in data:
                day_num = day_data.get("day")
                is_holiday = day_data.get("is_holiday", False)
                events = day_data.get("events", [])
                
                if events:
                    farsi_text = " - ".join([e["description"] for e in events])
                    english_text = translate_to_english(farsi_text)
                    events_english.append({
                        "d": day_num,
                        "t": english_text,
                        "h": is_holiday
                    })
            return events_english
    except Exception as e:
        print(f"Error in month {month}: {e}")
    return []

if __name__ == "__main__":
    year = 1404
    # ایجاد پوشه برای سازماندهی بهتر (اختیاری)
    # در اینجا فایل‌ها را در ریشه نگه می‌داریم تا دسترسی ESP32 ساده باشد
    
    for m in range(1, 13):
        month_data = fetch_month(year, m)
        output = {
            "year": year,
            "month": m,
            "events": month_data
        }
        
        filename = f"{m}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {filename}")
        time.sleep(1) # وقفه کوتاه برای جلوگیری از فشار به سرورها
