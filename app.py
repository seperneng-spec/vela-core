from copilot_quota import CopilotQuota
# สร้างระบบ — ตั้งค่าตามต้องการ
quota = CopilotQuota(limit_percent=100, reset_at_percent=90)
# ทุกครั้งที่มีการใช้งาน:
result = quota.use(1) # ใช้งาน 1%
print(result["message"])
# ดูสถานะตลอดเวลา:
print(quota.status())
