import requests
import json

TELEGRAM_TOKEN = "8048665417:AAEUWd5RCFZ3hEgOcHjnr4MRyKyvANf4-qs"
GEMINI_API_KEY = "AIzaSyA7hRs1veViDmfDqEkMZLkODp774jD6ZUE"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"أنت مستشار قانوني سعودي. أجب على السؤال التالي بذكر الأنظمة والمواد القانونية ذات الصلة وتحليل الوضع:\n\n{question}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "حدث خطأ، حاول مرة أخرى."

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    r = requests.get(url, params=params, timeout=35)
    return r.json()

def main():
    print("البوت يعمل...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                if chat_id and text:
                    if text == "/start":
                        send_message(chat_id, "مرحباً! أنا بوت الأنظمة القانونية السعودية. اكتب سؤالك وسأجيبك!")
                    else:
                        send_message(chat_id, "⏳ جاري البحث...")
                        response = ask_gemini(text)
                        send_message(chat_id, response)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
