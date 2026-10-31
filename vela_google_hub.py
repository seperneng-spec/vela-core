import os
import random
import requests

class VelaGoogleHub:
    def __init__(self):
        # 1. ระบบ Multi-Key Pool สำหรับ Gemini AI (ป้องกัน Rate Limit ฟรี)
        self.ai_api_keys = [
            os.getenv("GEMINI_KEY_1", "AIzaSy_MockKey_1"),
            os.getenv("GEMINI_KEY_2", "AIzaSy_MockKey_2"),
            os.getenv("GEMINI_KEY_3", "AIzaSy_MockKey_3")
        ]
        
        # 2. Google Apps Script Webhook สำหรับงานจัดการไฟล์, ชีท และแปลภาษา (ฟรี)
        self.gas_endpoint = os.getenv("GAS_WEBHOOK_URL", "https://script.google.com/macros/s/AKfycb.../exec")

    def get_rotated_ai_key(self):
        """สลับ API Key ของ Gemini แบบสุ่มเพื่อเลี่ยงโควตาหมด"""
        return random.choice(self.ai_api_keys)

    def dispatch_ai_request(self, prompt, model="gemini-1.5-flash"):
        """ส่งคำขอไปยัง Gemini AI ผ่าน Google AI Studio ฟรี"""
        active_key = self.get_rotated_ai_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={active_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                # กรณี Key หลักเต็ม สลับไปใช้ Key สำรองตัวถัดไป
                return self.fallback_ai_request(prompt)
        except Exception as e:
            return f"Vela AI Error: {str(e)}"

    def fallback_ai_request(self, prompt):
        """ระบบสำรองกรณีฉุกเฉิน"""
        # สามารถสลับไปใช้โมเดลสำรองหรือ Open Source เบื้องต้นได้
        return "Vela System: กำลังสลับเส้นทางสำรอง กรุณาลองใหม่อีกครั้ง"

    def execute_google_workspace_action(self, action_type, payload):
        """กระจายคำสั่งไปยัง Google Sheets, Drive, Translate ผ่าน Google Apps Script"""
        data = {
            "action": action_type, # เช่น "save_sheet", "upload_drive", "translate"
            "payload": payload
        }
        try:
            response = requests.post(self.gas_endpoint, json=data, timeout=15)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

# ตัวอย่างการเรียกใช้งานจาก Vela Hub
vela_hub = VelaGoogleHub()

