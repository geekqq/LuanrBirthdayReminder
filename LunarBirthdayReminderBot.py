import json
import requests
from datetime import date
from lunardate import LunarDate
import os

CONFIG_FILE = "birthdays.json"

TG_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TEST_MODE = os.environ.get("TEST_MODE") == "1"


def send_telegram(msg):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    url = f"hhttps://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(
        url, json={
            "chat_id": TG_CHAT_ID,
            "text": msg
        }
    )

def lunar_to_solar(year, month, day):
    return LunarDate(year, month, day).toSolarDate()

def main():
    today = date.today()

    with open(CONFIG_FILE, encoding="utf-8") as f:
        birthdays = json.load(f)

    for p in birthdays:
        for year in (today.year, today.year + 1):
            solar = lunar_to_solar(year, p["lunar_month"], p["lunar_day"])
            delta = (solar - today).days
            if TEST_MODE or delta in p["notify_days_before"]:
                when = "今天" if delta == 0 else f"{delta} 天后"
                msg = (
                    f"🎂 农历生日提醒\n"
                    f"{p['name']} 的农历生日是 {when}\n"
                    f"📅 公历：{solar}"
                )
                send_telegram(msg)

if __name__ == "__main__":
    main()