import requests
import json
import time

def translate_to_english(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fa&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        return r.json()[0][0][0]
    except:
        return text

def main():
    year = 1404  # می‌توانید این را داینامیک کنید
    for month in range(1, 13):
        print(f"Fetching Month {month}...")
        try:
            # استفاده از API مستقیم برای دریافت کل ماه
            response = requests.get(f"https://holidayapi.ir/jalali/{year}/{month}", timeout=15)
            if response.status_code == 200:
                data = response.json()
                events_list = []
                for day_info in data:
                    day_num = day_info.get("day")
                    is_holiday = day_info.get("is_holiday", False)
                    events = day_info.get("events", [])
                    if events:
                        farsi_text = " - ".join([e["description"] for e in events])
                        english_text = translate_to_english(farsi_text)
                        events_list.append({"d": day_num, "t": english_text, "h": is_holiday})
                
                with open(f"{month}.json", 'w', encoding='utf-8') as f:
                    json.dump({"year": year, "month": month, "events": events_list}, f, ensure_ascii=False, indent=2)
            time.sleep(2) # وقفه برای جلوگیری از مسدود شدن
        except Exception as e:
            print(f"Error in month {month}: {e}")

if __name__ == "__main__":
    main()
