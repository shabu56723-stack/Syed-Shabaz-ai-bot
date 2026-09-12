from flask import Flask, request, jsonify
import requests, os
app = Flask(__name__)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "syed_king_7865")

def get_ai_reply(msg):
    m=msg.lower()
    if any(w in m for w in ["hello","hi","salam","hey"]):
        return "Salam Boss! 👑 Main SYED SHABAZ ka AI Assistant hu 💜\n1.COLLAB\n2.PRICE\n3.INSTA @SYED_SHABAZ__7865__95"
    if "collab" in m:
        return "🔥 COLLAB ke liye @SYED_SHABAZ__7865__95 pe DM karo!"
    if "price" in m:
        return "💰 Best Price ke liye DM @SYED_SHABAZ__7865__95"
    return f"Thanks '{msg}' mil gaya Boss! SYED reply karega 👑"

@app.route('/')
def home(): return "<h1>SYED SHABAZ BOT RUNNING 👑</h1>"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method=='GET':
        if request.args.get('hub.verify_token')==VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Failed",403
    try:
        data=request.json
        v=data['entry'][0]['changes'][0]['value']
        if 'messages' in v:
            body=v['messages'][0]['text']['body']
            frm=v['messages'][0]['from']
            reply=get_ai_reply(body)
            url=f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            payload={"messaging_product":"whatsapp","to":frm,"text":{"body":reply}}
            requests.post(url,json=payload,headers=headers)
    except: pass
    return jsonify(ok=True)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
