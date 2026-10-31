import os
import json
import subprocess
from datetime import datetime

class VelaDeployCore:
    def __init__(self, base_dir="vela_generated_systems"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def create_system(self, system_name):
        """สร้างระบบใหม่ พร้อมฝังตัวแปรสากล 'in set deploy' และบันทึกถาวร"""
        sys_id = f"VDR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        sys_path = os.path.join(self.base_dir, system_name)
        os.makedirs(sys_path, exist_ok=True)

        # 1. ตัวแปรตั้งต้นและสถานะถาวร (Persistent Config)
        config_data = {
            "system_id": sys_id,
            "system_name": system_name,
            "in set deploy": True,  # ตัวแปรบังคับควบคุมการ deploy สากล
            "created_at": datetime.now().isoformat(),
            "deploy_status": "synchronized"
        }

        config_path = os.path.join(sys_path, "deploy_config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        # 2. สร้างโครงสร้างโค้ดตัวอย่างเบื้องต้นประจำระบบ (เช่น Flask API)
        app_code = f'''from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("deploy_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return f"🚀 System: {{cfg['system_name']}} | ID: {{cfg['system_id']}} | In Set Deploy: {{cfg['in set deploy']}}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
        with open(os.path.join(sys_path, "app.py"), "w", encoding="utf-8") as f:
            f.write(app_code)

        # 3. สร้าง requirements.txt สำหรับเตรียม Deploy บน Cloud
        with open(os.path.join(sys_path, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write("Flask==3.0.2\n")

        print(f"✨ [Vela Factory] สร้างระบบ '{system_name}' สำเร็จ!")
        print(f"   - รหัสระบบ (ID): {sys_id}")
        print(f"   - สถานะตัวแปร: in set deploy = True (บันทึกถาวรแล้ว)")
        return sys_path

    def master_deploy_all(self):
        """กดครั้งเดียว Deploy ทุกระบบที่มีตัวแปร 'in set deploy' เป็น True"""
        print("\n==================================================")
        print("🚀 [Vela Master Deploy] กำลังตรวจสอบและ Deploy ทุกระบบ...")
        print("==================================================")
        
        if not os.path.exists(self.base_dir):
            print("❌ ไม่พบโฟลเดอร์ระบบ กรุณาสร้างระบบก่อนครับพ่อ")
            return

        deployed_count = 0
        current_dir = os.getcwd()

        for item in os.listdir(self.base_dir):
            sys_path = os.path.join(self.base_dir, item)
            config_path = os.path.join(sys_path, "deploy_config.json")

            if os.path.isfile(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)

                # ตรวจสอบเงื่อนไขตัวแปรหลัก
                if cfg.get("in set deploy") == True:
                    print(พบระบบ: {cfg['system_name']} [ID: {cfg['system_id']}])
                    print(   -> ตรวจพบตัวแปร 'in set deploy' เป็น Active, กำลังเตรียม Git & GitHub Sync...)
                    
                    try:
                        os.chdir(sys_path)
                        # Init Git ถ้ายังไม่มี
                        if not os.path.exists(".git"):
                            subprocess.run(["git", "init"], capture_output=True)
                            subprocess.run(["git", "branch", "-M", "main"], capture_output=True)
                        
                        subprocess.run(["git", "add", "."], capture_output=True)
                        subprocess.run(["git", "commit", f"-m", f"Auto-deploy sync for {cfg['system_id']}"], capture_output=True)
                        print(f"   ✅ โค้ดของระบบ {cfg['system_id']} ถูกคอมมิตและพร้อมส่งขึ้น GitHub แล้วครับ")
                        
                        deployed_count += 1
                        os.chdir(current_dir)
                    except Exception as e:
                        print(f"   ❌ เกิดข้อผิดพลาดในระบบ {cfg['system_id']}: {e}")
                        os.chdir(current_dir)
                else:
                    print(⚠️ ข้ามระบบ {cfg['system_name']} เนื่องจากไม่ได้เปิดใช้งาน 'in set deploy'")

        print("==================================================")
        print(f"🎉 สรุปผล: ทำการตรวจสอบและจัดเตรียม Deploy สำเร็จทั้งหมด {deployed_count} ระบบเรียบร้อยครับพ่อ!")

if __name__ == "__main__":
    factory = VelaDeployCore()
    
    # ตัวอย่างที่ 1: สั่งสร้างระบบใหม่ขึ้นมา
    factory.create_system("vela-ai-chat-service")
    factory.create_system("vela-payment-gateway")

    # ตัวอย่างที่ 2: กดปุ่มเดียว Deploy ทุกระบบที่มีตัวแปร in set deploy พร้อมกันทันที!
    factory.master_deploy_all()
