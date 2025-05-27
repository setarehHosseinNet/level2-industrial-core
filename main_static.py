# فایل: main_static.py
from core import HeatTracker, SetpointCalculator, QualityEvaluator
from db import DatabaseManager

# راه‌اندازی کلاس‌ها
tracker = HeatTracker()
db = DatabaseManager()

# ثبت یک ذوب جدید
heat_id = "H001"
start_time = "2025-05-27 12:00:00"
tracker.register_heat(heat_id, start_time)
db.insert_heat(heat_id, start_time)

# ثبت رویدادها
events = [
    {"type": "entered_LRF", "position": "LRF", "timestamp": "2025-05-27 12:05:00"},
    {"type": "entered_CCM", "position": "CCM", "timestamp": "2025-05-27 12:20:00"}
]

for event in events:
    tracker.add_event(heat_id, event)
    db.add_event(heat_id, event["type"], event["position"], event["timestamp"])

# محاسبه دمای هدف
setpoint_calc = SetpointCalculator()
target_temp = setpoint_calc.calculate(length=1.6, width=1.6, material="ST37")
print("Target temperature:", target_temp)

# ارزیابی کیفیت
quality_eval = QualityEvaluator()
print("Heat Quality:", quality_eval.evaluate(temp_end=870))

# تکمیل ذوب
tracker.complete_heat(heat_id)
db.update_heat_status(heat_id, "Completed")

# چاپ اطلاعات نهایی ذوب
print(tracker.heats[heat_id])
db.close()
