from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")
VERIFY_TOKEN = "princejule123"

@app.route("/")
def home():
    return "Bot en ligne!"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Erreur", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_number = msg['from']
            text = msg['text']['body']
            reply = f"Salut! Tu as dit: {text} - C'est ton bot auto 🤖"
            url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
            headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp","to": from_number,"text": {"body": reply}}
            requests.post(url, headers=headers, json=payload)
    except:
        pass
    return "OK", 200
