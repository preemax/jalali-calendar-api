import requests
from bs4 import BeautifulSoup
import json

def fetch_time_ir(year, month):
    url = f"https://www.time.ir/fa/event/list/0/{year}/{month}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        events_list = []
        # پیدا کردن لیست مناسبت‌ها در ساختار جدید Time.ir
        items = soup.select('ul.list-unstyled > li')
        
        for item in items:
            day_num_el = item.find('span')
            if not day_num_el: continue
            
            day_text = day_num_el.text.strip()
            # استخراج متن مناسبت (پاک کردن شماره روز از ابتدای متن)
            full_text = item.get_text(strip=True)
            event_text = full_text.replace(day_text, "", 1).strip()
            
            # تشخیص تعطیلی از روی کلاس CSS یا رنگ قرمز
            is_holiday = "eventHoliday" in item.get('class', []) or (item.find('span', class_='eventHoliday') is not None)
            
            events_list.append({
                "d": int(day_text),
                "t": event_text,
                "h": is_holiday
            })
            
        return {"year": year, "month": month, "events": events_list}
    except Exception as e:
        print(f"Error: {e}")
        return {"year": year, "month": month, "events": [], "error": str(e)}

if __name__ == "__main__":
    data = fetch_time_ir(1404, 10)
    with open('10.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
