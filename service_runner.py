# فایل: service_runner.py
import time
import logging
from core import HeatTracker, SetpointCalculator, QualityEvaluator
from db import DatabaseManager
from dcccom_simulator import DCCCOMSimulator
from datetime import datetime

# پیکربندی لاگر
logging.basicConfig(
    filename="heat_tracking.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# راه‌اندازی اجزای سیستم
tracker = HeatTracker()
db = DatabaseManager()
sim = DCCCOMSimulator()
setpoint_calc = SetpointCalculator()
quality_eval = QualityEvaluator()

logging.info("🔥 سرویس Heat Tracking آغاز شد")

try:
    while True:
        heat_id = f"H_SRV_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        start_time = datetime.now().isoformat()
        tracker.register_heat(heat_id, start_time)
        db.insert_heat(heat_id, start_time)

        data = sim.read_all()
        timestamp = datetime.now().isoformat()

        for tag_name, value in data.items():
            event_type = tag_name.split(".")[-1]
            position = value if "Position" in tag_name else ""
            tracker.add_event(heat_id, {"type": event_type, "position": position, "timestamp": timestamp})
            db.add_event(heat_id, event_type, position, timestamp)
            logging.info(f"{heat_id} | {event_type} at {position} = {value}")

        # تحلیل‌ها
        target_temp = setpoint_calc.calculate(length=1.6, width=1.6, material="ST37")
        quality = quality_eval.evaluate(temp_end=870)
        logging.info(f"{heat_id} | TargetTemp={target_temp} | Quality={quality}")

        # پایان ذوب
        tracker.complete_heat(heat_id)
        db.update_heat_status(heat_id, "Completed")

        logging.info(f"{heat_id} | Heat completed\n")
        time.sleep(10)

except KeyboardInterrupt:
    logging.warning("❗ سرویس توسط کاربر متوقف شد")
finally:
    db.close()
    logging.info("🔚 اتصال پایگاه داده بسته شد")
