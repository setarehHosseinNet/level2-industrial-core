# فایل: main_combined.py
from core import HeatTracker, SetpointCalculator, QualityEvaluator
from db import DatabaseManager
from dcccom_simulator import DCCCOMSimulator
from datetime import datetime
import time

# راه‌اندازی کلاس‌ها
tracker = HeatTracker()
db = DatabaseManager()
sim = DCCCOMSimulator()
setpoint_calc = SetpointCalculator()
quality_eval = QualityEvaluator()

try:
    for i in range(2):  # اجرای دو چرخه‌ی نمونه
        # ایجاد heat_id و زمان شروع
        heat_id = f"H_COMB_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now().isoformat()
        tracker.register_heat(heat_id, start_time)
        db.insert_heat(heat_id, start_time)

        # شبیه‌سازی خواندن داده‌ها از DCCCOM
        data = sim.read_all()
        timestamp = datetime.now().isoformat()

        for tag_name, value in data.items():
            event_type = tag_name.split(".")[-1]
            position = value if "Position" in tag_name else ""
            tracker.add_event(heat_id, {"type": event_type, "position": position, "timestamp": timestamp})
            db.add_event(heat_id, event_type, position, timestamp)
            print(f"{tag_name}: {value}")

        # افزودن رویدادهای ایستا
        static_events = [
            {"type": "entered_LRF", "position": "LRF", "timestamp": datetime.now().isoformat()},
            {"type": "entered_CCM", "position": "CCM", "timestamp": datetime.now().isoformat()}
        ]
        for event in static_events:
            tracker.add_event(heat_id, event)
            db.add_event(heat_id, event["type"], event["position"], event["timestamp"])

        # محاسبه و ارزیابی
        target_temp = setpoint_calc.calculate(length=1.6, width=1.6, material="ST37")
        print("Target temperature:", target_temp)
        quality = quality_eval.evaluate(temp_end=870)
        print("Heat Quality:", quality)

        # تکمیل ذوب
        tracker.complete_heat(heat_id)
        db.update_heat_status(heat_id, "Completed")
        print("Final Heat Info:", tracker.heats[heat_id])

        print("⏳ Wait 5 sec before next heat\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Stopped by user.")
finally:
    db.close()
