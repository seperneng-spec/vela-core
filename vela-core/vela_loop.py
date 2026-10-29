import json
import os

class VelaLoopSystem:
    def __init__(self):
        self.state_file = os.path.expanduser("~/vela-core/system_state.json")

    def process_outbound(self, task_name, payload_data):
        print(f"[Vela Outbound] 🚀 กำลังแยกประเภทและส่งงานออกไป: {task_name}")
        outbound_packet = {
            "task": task_name,
            "status": "dispatched",
            "data": payload_data,
            "callback_url": "https://api.vela-core.local/callback"
        }
        return outbound_packet

    def process_inbound(self, response_data):
        print(f"[Vela Inbound] 📥 ได้รับข้อมูล/ผลลัพธ์กลับเข้ามาในระบบแล้ว!")
        
        # บันทึกสถานะกลับเข้าสู่ระบบภายในของ Vela Core
        state = {
            "last_sync": response_data,
            "status": "integrated_successfully"
        }
        
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
            
        print(f"[Vela Core] ✅ อัปเดตสถานะระบบภายในเรียบร้อยที่: {self.state_file}")
        return state

if __name__ == "__main__":
    vela_loop = VelaLoopSystem()
    
    # 1. จำลองการส่งออกไปต่อยอด
    packet = vela_loop.process_outbound("Analyze_And_Deploy", {"target": "Lampang_Node", "action": "sync"})
    
    # 2. จำลองเมื่อปลายทางส่งผลลัพธ์กลับเข้ามาในระบบของ Vela
    simulated_response = {
        "task_id": "TASK-9921",
        "result": "success",
        "message": "ประมวลผลภายนอกสำเร็จและส่งข้อมูลกลับเข้า Vela Core แล้ว"
    }
    
    vela_loop.process_inbound(simulated_response)
