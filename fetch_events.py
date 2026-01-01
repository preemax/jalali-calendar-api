import requests
from bs4 import BeautifulSoup
import json

def fetch_time_ir(year, month):
    url = f"https://www.time.ir/fa/event/list/0/{year}/{month}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    events_list = []
    # پیدا کردن تمام ردیف‌های مناسبت‌ها
    items = soup.find_all('li', class_='eventCurrentMonth')
    
    for item in items:
        try:
            # استخراج شماره روز
            day_text = item.find('span').text.strip()
            # استخراج متن مناسبت
            event_text = item.contents[2].strip()
            # تشخیص تعطیل بودن (معمولاً با رنگ قرمز در سایت مشخص می‌شود)
            is_holiday = "eventHoliday" in item.get('class', [])
            
            events_list.append({
                "d": int(day_text),
                "t": event_text,
                "h": is_holiday
            })
        except:
            continue
            
    return {
        "year": year,
        "month": month,
        "events": events_list
    }

if __name__ == "__main__":
    # فعلاً برای ماه ۱۰ تست می‌کنیم
    data = fetch_time_ir(1404, 10)
    with open('10.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
