import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8048665417:AAEUWd5RCFZ3hEgOcHjnr4MRyKyvANf4-qs"
GEMINI_API_KEY = "AIzaSyA7hRs1veViDmfDqEkMZLkODp774jD6ZUE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

logging.basicConfig(level=logging.INFO)

def ask_gemini(question):
    prompt = f"""أنت مستشار قانوني متخصص في الأنظمة السعودية. أجب على السؤال التالي بذكر:
1. الأنظمة ذات الصلة واسم النظام ورقم المادة
2. النص القانوني
3. الجهة المختصة
4. تحليل الوضع
5. التوصية

السؤال: {question}"""
    
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048}}
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "حدث خطأ، حاول مرة أخرى."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏛️ مرحباً! أنا بوت الأنظمة القانونية السعودية.\n\nاكتب سؤالك أو وضعك وسأبحث لك في الأنظمة السعودية!")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ جاري البحث في الأنظمة الس​​​​​​​​​​​​​​​​
