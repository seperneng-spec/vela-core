import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_KEY_1", "AIzaSy_MockKey...")
GAS_WEBHOOK_URL = os.getenv("GAS_WEBHOOK_URL", "https://script.google.com/macros/s/AKfycb.../exec")

class CristalPromptEngine:
    @staticmethod
    def generate_sticker_pipeline(concept):
        """ระบบเจน Prompt สติ๊กเกอร์ แบบ Dual-Track (Character + Meme)"""
        system_prompt = f"""
        คุณคือผู้เชี่ยวชาญการออกแบบ Sticker และ Meme สำหรับ Project Cristal 
        จงนำแนวคิดนี้: '{concept}' มาสร้าง Prompt 2 รูปแบบในรูปแบบ JSON:
        1. "character_track": Prompt ภาษาอังกฤษสำหรับสร้างภาพตัวละครหลัก (Detail, Lighting, Expressions, Vector Style, White Background)
        2. "meme_track": Prompt ข้อความมุก/แก๊กภาษาไทยสั้นๆ ที่เหมาะกับการนำไปแปะบนสติ๊กเกอร์

        ตอบกลับเฉพาะ JSON รูปแบบนี้เท่านั้น:
        {{
            "character_prompt": "...",
            "meme_text": "..."
        }}
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": system_prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                raw_text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                # ทำความสะอาดข้อมูล JSON
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
            else:
                return {"character_prompt": concept, "meme_text": concept}
        except Exception as e:
            return {"error": str(e)}

@app.route("/vela/cristal/generate", methods=["POST"])
def cristal_generate():
    req_data = request.json or {}
    concept = req_data.get("concept", "แมวส้มกวนๆ")
    user_id = req_data.get("user", "พ่อธันวา")

    # 1. เจน Prompt ผ่าน Cristal Engine
    result = CristalPromptEngine.generate_sticker_pipeline(concept)

    # 2. ส่งไปบันทึกใน Google Sheets ผ่าน Apps Script (คลัง Cristal)
    sheet_payload = {
        "action": "save_sheet",
        "payload": {
            "spreadsheetId": os.getenv("SPREADSHEET_ID", "YOUR_SHEET_ID"),
            "sheetName": "CristalStudio",
            "user": user_id,
            "concept": concept,
            "character_prompt": result.get("character_prompt", ""),
            "meme_text": result.get("meme_text", "")
        }
    }
    try:
        requests.post(GAS_WEBHOOK_URL, json=sheet_payload, timeout=10)
    except:
        pass

    return jsonify({
        "status": "success",
        "project": "Cristal Sticker Studio",
        "concept": concept,
        "outputs": result
    })

if __name__ == "__main__":
    print("==================================================")
    print("   VELA Core -> PROJECT CRISTAL CONNECTED         ")
    print("==================================================")
    app.run(host="0.0.0.0", port=5081, debug=False)

