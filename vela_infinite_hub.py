# 1. ปิด Python ตัวเก่า
pkill -f python3

# 2. เขียนโค้ดรวมศูนย์ (Vela + Google + GitHub + Cristal)
cat << 'EOF' > vela_infinite_hub.py
import os
import random
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATIONS ---
GEMINI_API_KEYS = [
    os.getenv("GEMINI_KEY_1", "AIzaSy_MockKey_1"),
    os.getenv("GEMINI_KEY_2", "AIzaSy_MockKey_2")
]
GAS_WEBHOOK_URL = os.getenv("GAS_WEBHOOK_URL", "https://script.google.com/macros/s/AKfycb.../exec")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token_here")
GITHUB_REPO = os.getenv("GITHUB_REPO", "seperneng-spec/coilpo") # หรือชื่อ repo ของพ่อ

class VelaMasterEngine:
    @staticmethod
    def get_ai_key():
        valid_keys = [k for k in GEMINI_API_KEYS if "MockKey" not in k]
        return random.choice(valid_keys) if valid_keys else GEMINI_API_KEYS[0]

    @staticmethod
    def ask_gemini(prompt):
        key = VelaMasterEngine.get_ai_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(url, json=payload, timeout=12)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"[Vela AI Warning]: Code {res.status_code}"
        except Exception as e:
            return f"[Vela Error]: {str(e)}"

    @staticmethod
    def fetch_github_latest_commit():
        """ดึงข้อมูล Commit ล่าสุดจาก GitHub Repository coilpo"""
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN != "your_github_token_here" else {}
        url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                commits = res.json()
                if commits and len(commits) > 0:
                    latest = commits[0]
                    return {
                        "sha": latest['sha'][:7],
                        "message": latest['commit']['message'],
                        "author": latest['commit']['author']['name']
                    }
            return {"status": "no_connection", "message": "Could not fetch GitHub commits"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# --- ENDPOINTS ---
@app.route("/vela/webhook", methods=["POST"])
def vela_webhook():
    req_data = request.json or {}
    message = req_data.get("message", "สวัสดี Vela")
    user = req_data.get("user", "พ่อธันวา")

    # ถ้าพ่อพิมพ์ถามเกี่ยวกับ GitHub ให้ดึงข้อมูลล่าสุดจาก coilpo มาตอบด้วย
    context_extra = ""
    if "git" in message.lower() or "coilpo" in message.lower() or "โค้ด" in message.lower():
        gh_info = VelaMasterEngine.fetch_github_latest_commit()
        context_extra = f"\n[ข้อมูลล่าสุดจาก GitHub {GITHUB_REPO}]: Commit ล่าสุด ({gh_info.get('sha')}) - {gh_info.get('message')}"

    full_prompt = f"{message}\n{context_extra}"
    ai_reply = VelaMasterEngine.ask_gemini(full_prompt)

    # บันทึก Log ลง Google Sheets ผ่าน GAS
    sheet_payload = {
        "action": "save_sheet",
        "payload": {
            "spreadsheetId": os.getenv("SPREADSHEET_ID", "YOUR_SHEET_ID"),
            "sheetName": "VelaMasterLogs",
            "user": user,
            "message": message,
            "response": ai_reply
        }
    }
    try:
        requests.post(GAS_WEBHOOK_URL, json=sheet_payload, timeout=8)
    except:
        pass

    return jsonify({
        "status": "success",
        "system": "Vela Master Core + Coilpo Bridge",
        "sender": user,
        "reply": ai_reply
    })

@app.route("/vela/github/webhook", methods=["POST"])
def github_webhook_receiver():
    """รับสัญญาณ Push Event จาก GitHub (Webhook) เมื่อมีการอัปเดตโค้ดใน coilpo"""
    event = request.headers.get("X-GitHub-Event", "ping")
    payload = request.json or {}
    
    if event == "push":
        repo_name = payload.get("repository", {}).get("full_name", "Unknown")
        pusher = payload.get("pusher", {}).get("name", "Unknown")
        print(f"🔔 [GitHub Event]: มีการ Push โค้ดใหม่เข้าสู่ {repo_name} โดย {pusher}")
        
    return jsonify({"status": "received", "event": event})

if __name__ == "__main__":
    print("==================================================")
    print("   VELA MASTER CORE + COILPO BRIDGE INITIALIZED   ")
    print("==================================================")
    app.run(host="0.0.0.0", port=5080, debug=False)
EOF

# 3. ติดตั้งไลบรารีและรันเซิร์ฟเวอร์
pip install flask requests > /dev/null 2>&1
python3 vela_infinite_hub.py
# 1. ติดตั้ง pymongo เพิ่ม
pip install pymongo > /dev/null 2>&1

# 2. อัปเดตไฟล์ vela_infinite_hub.py
cat << 'EOF' > vela_infinite_hub.py
import os
import random
import requests
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURATIONS ---
GEMINI_API_KEYS = [
    os.getenv("GEMINI_KEY_1", "AIzaSy_MockKey_1"),
    os.getenv("GEMINI_KEY_2", "AIzaSy_MockKey_2")
]
GAS_WEBHOOK_URL = os.getenv("GAS_WEBHOOK_URL", "https://script.google.com/macros/s/AKfycb.../exec")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token_here")
GITHUB_REPO = os.getenv("GITHUB_REPO", "seperneng-spec/coilpo")

# --- MONGODB CONNECTION ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = mongo_client["vela_master_db"]
    logs_collection = db["vela_logs"]
    print("🟢 [MongoDB]: Connected successfully to database 'vela_master_db'")
except Exception as e:
    mongo_client = None
    print(f"🔴 [MongoDB Error]: {e}")

class VelaMasterEngine:
    @staticmethod
    def get_ai_key():
        valid_keys = [k for k in GEMINI_API_KEYS if "MockKey" not in k]
        return random.choice(valid_keys) if valid_keys else GEMINI_API_KEYS[0]

    @staticmethod
    def ask_gemini(prompt):
        key = VelaMasterEngine.get_ai_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(url, json=payload, timeout=12)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"[Vela AI Warning]: Code {res.status_code}"
        except Exception as e:
            return f"[Vela Error]: {str(e)}"

    @staticmethod
    def fetch_github_latest_commit():
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN != "your_github_token_here" else {}
        url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                commits = res.json()
                if commits and len(commits) > 0:
                    latest = commits[0]
                    return {
                        "sha": latest['sha'][:7],
                        "message": latest['commit']['message'],
                        "author": latest['commit']['author']['name']
                    }
            return {"status": "no_connection"}
        except:
            return {"status": "error"}

@app.route("/vela/webhook", methods=["POST"])
def vela_webhook():
    req_data = request.json or {}
    message = req_data.get("message", "สวัสดี Vela")
    user = req_data.get("user", "พ่อธันวา")

    context_extra = ""
    if "git" in message.lower() or "coilpo" in message.lower() or "โค้ด" in message.lower():
        gh_info = VelaMasterEngine.fetch_github_latest_commit()
        context_extra = f"\n[ข้อมูลล่าสุดจาก GitHub {GITHUB_REPO}]: Commit ล่าสุด ({gh_info.get('sha')}) - {gh_info.get('message')}"

    full_prompt = f"{message}\n{context_extra}"
    ai_reply = VelaMasterEngine.ask_gemini(full_prompt)

    # 1. บันทึกข้อมูลลง MongoDB
    log_document = {
        "user": user,
        "message": message,
        "reply": ai_reply,
        "system": "Vela-Core + MongoDB"
    }
    if mongo_client:
        try:
            logs_collection.insert_one(log_document)
        except Exception as e:
            print(f"MongoDB Insert Error: {e}")

    # 2. สำรองข้อมูลส่งเข้า Google Sheets ผ่าน GAS (ตามเดิม)
    sheet_payload = {
        "action": "save_sheet",
        "payload": {
            "spreadsheetId": os.getenv("SPREADSHEET_ID", "YOUR_SHEET_ID"),
            "sheetName": "VelaMasterLogs",
            "user": user,
            "message": message,
            "response": ai_reply
        }
    }
    try:
        requests.post(GAS_WEBHOOK_URL, json=sheet_payload, timeout=5)
    except:
        pass

    return jsonify({
        "status": "success",
        "system": "Vela Master Core + MongoDB + Coilpo Bridge",
        "sender": user,
        "reply": ai_reply
    })

if __name__ == "__main__":
    print("==================================================")
    print("   VELA MASTER CORE + MONGODB INITIALIZED         ")
    print("==================================================")
    app.run(host="0.0.0.0", port=5080, debug=False)
EOF

# 3. รันเซิร์ฟเวอร์ใหม่
python3 vela_infinite_hub.py

