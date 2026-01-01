import requests
from bs4 import BeautifulSoup
import json

def fetch_time_ir(year, month):
    url = f"https://www.time.ir/fa/event/list/0/{year}/{month}"
    # استفاده از یک User-Agent واقعی‌تر برای دور زدن محدودیت‌ها
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        events_list = []
        # جستجوی تمام تگ‌های li که حاوی اطلاعات روز هستند
        items = soup.find_all('li')
        
        for item in items:
            # پیدا کردن شماره روز (در سایت تایم دات آی آر در تگ span یا داخل متن است)
            day_num_el = item.find('span')
            if not day_num_el or not day_num_el.text.strip().isdigit():
                continue
            
            day_text = day_num_el.text.strip()
            # استخراج متن مناسبت
            event_text = item.get_text(strip=True).replace(day_text, "", 1).strip()
            
            # تشخیص تعطیلی: چک کردن رنگ قرمز یا کلاس Holiday
            style = item.get('style', '')
            cl = item.get('class', [])
            is_holiday = "eventHoliday" in cl or "color:red" in style.replace(" ", "").lower()
            
            if event_text:
                events_list.append({
                    "d": int(day_text),
                    "t": event_text,
                    "h": is_holiday
                })
            
        return {"year": year, "month": month, "events": events_list}
    except Exception as e:
        return {"year": year, "month": month, "events": [], "error": str(e)}

if __name__ == "__main__":
    data = fetch_time_ir(1404, 10)
    # ذخیره فایل با فرمت UTF-8 واقعی
    with open('10.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
