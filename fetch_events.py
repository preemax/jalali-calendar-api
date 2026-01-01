import requests
import json
import time

def translate_to_english(text):
    # این یک ترفند برای ترجمه ساده با استفاده از یک API عمومی است
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fa&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        return r.json()[0][0][0]
    except:
        return text # اگر ترجمه نشد، خود متن را برگردان

def fetch_and_translate(year, month):
    events_english = []
    
    # ما کل روزهای ماه را چک می‌کنیم (۱ تا ۳۱)
    for day in range(1, 32):
        api_url = f"https://holidayapi.ir/jalali/{year}/{month}/{day}"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                is_holiday = data.get("is_holiday", False)
                events = data.get("events", [])
                
                if events:
                    # ترکیب تمام مناسبت‌های یک روز در یک رشته
                    farsi_text = " - ".join([e["description"] for e in events])
                    # ترجمه به انگلیسی
                    english_text = translate_to_english(farsi_text)
                    
                    events_english.append({
                        "d": day,
                        "t": english_text,
                        "h": is_holiday
                    })
                    print(f"Day {day}: Translated.")
                    time.sleep(0.5) # کمی وقفه برای مسدود نشدن توسط گوگل
        except Exception as e:
            print(f"Error on day {day}: {e}")
            
    return {
        "year": year,
        "month": month,
        "events": events_english
    }

if __name__ == "__main__":
    # برای ماه ۱۰ (دی) سال ۱۴۰۴
    final_data = fetch_and_translate(1404, 10)
    with open('10.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
