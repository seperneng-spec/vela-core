import json
import sys

def analyze_event(raw_text):
    # จำลองระบบวิเคราะห์เหตุการณ์และแยกพิกัด
    print(f"[*] กำลังวิเคราะห์เหตุการณ์: '{raw_text}'")
    
    # ตัวอย่างการจำกัดโครงสร้างข้อมูลที่วิเคราะห์ได้
    event_data = {
        "event_type": "Action_Trigger",
        "target_location": "Ban Pao, Lampang, Thailand",
        "coordinates": {"lat": 18.2888, "lng": 99.4923},
        "action_payload": "cd ~/vela-core && python3 main.py --execute"
    }
    
    return event_data

def generate_auto_script(data):
    script_content = f"""# === AUTO-GENERATED EXECUTION SCRIPT ===
# พิกัดเป้าหมาย: {data['target_location']} ({data['coordinates']['lat']}, {data['coordinates']['lng']})
# ประเภทการกระทำ: {data['event_type']}

echo "🚀 กำลังส่งการกระทำไปยังปลายทาง..."
{data['action_payload']}
echo "✅ ดำเนินการเสร็จสิ้นที่พิกัด {data['target_location']}"
"""
    return script_content

if __name__ == "__main__":
    sample_text = "ตรวจสอบระบบเซิร์ฟเวอร์และสั่งรันสคริปต์ที่บ้านป่าเป้า ลำปาง"
    result = analyze_event(sample_text)
    
    print("\n[+] ผลลัพธ์การวิเคราะห์พิกัด:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n[+] โค้ดสำหรับก๊อปปี้ไปรันอัตโนมัติ:")
    print("-" * 40)
    auto_code = generate_auto_script(result)
    print(auto_code)
    print("-" * 40)
