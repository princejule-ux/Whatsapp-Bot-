from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")
VERIFY_TOKEN = "princejule123"

def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

@app.route("/")
def home():
    return "BOT PURGE CLAN EN LIGNE 🔴 - BY MD"

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
            text = msg['text']['body'].lower()

            # --- LOGIQUE PURGE CLAN ---
            if "salut" in text or "slt" in text:
                reply = "🩸 Salut guerrier! Bienvenue chez PURGE SERVICE. Tape MENU"
            elif "menu" in text:
                reply = "📋 *MENU PURGE BOT*\n1️⃣ PRIX\n2️⃣ HORAIRES\n3️⃣ COMMANDE\n4️⃣ SERMENT\n5️⃣ MD"
            elif "prix" in text:
                reply = "💰 Prix à partir de 2000F. Dis ce que tu veux."
            elif "serment" in text:
                reply = "🩸 *SERMENT PURGE* 🩸\nJe jure loyauté à MD et au clan PURGE. PURGE À VIE."
            elif "ban" in text:
                reply = f"🚫 *TRIBUNAL PURGE* - Le traître a été banni par MD."
            elif "md" in text:
                reply = "👑 Patron suprême: MD\n🔴 PURGE CLAN - Loyauté, Force, Respect"
            else:
                reply = f"Salut! Tu as dit: {msg['text']['body']}. Tape MENU pour voir les commandes."

            send_message(from_number, reply)
    except Exception as e:
        print(f"Erreur: {e}")

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
