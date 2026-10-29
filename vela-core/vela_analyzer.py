import json
import os

class VelaEventSystem:
    def __init__(self):
        self.location = "Ban Pao, Mueang Lampang, Thailand"
        self.coords = {"lat": 18.2888, "lng": 99.4923}

    def analyze(self, action_target):
        print(f"[Vela Core] 🤖 กำลังวิเคราะห์เหตุการณ์สำหรับ: '{action_target}'")
        
        # จำลองการสร้าง Action Payload สำหรับนำไปรันอัตโนมัติ
        payload = f"cd ~/vela-core && echo 'Executing action for: {action_target}' && git status"
        
        report = {
            "system": "Vela Core",
            "target": action_target,
            "location": self.location,
            "coordinates": self.coords,
            "auto_command": payload
        }
        return report

    def save_and_output(self, report):
        output_path = os.path.expanduser("~/vela-core/last_event.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print("\n=== [Vela Core Analysis Result] ===")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("====================================")
        print("\n[+] ก๊อปปี้คำสั่งนี้ไปรันอัตโนมัติได้ทันที:")
        print(f"👉 {report['auto_command']}")

if __name__ == "__main__":
    vela = VelaEventSystem()
    event_result = vela.analyze("ตรวจสอบระบบสแกมเมอร์และอัปเดตสคริปต์ฐานทัพลำปาง")
    vela.save_and_output(event_result)
