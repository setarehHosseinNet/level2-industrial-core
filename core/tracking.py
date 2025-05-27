# فایل: core/tracking.py
class HeatTracker:
    def __init__(self):
        self.heats = {}

    def register_heat(self, heat_id, time_start):
        self.heats[heat_id] = {
            "start": time_start,
            "events": [],
            "status": "Active",
            "position": None,
            "last_update": time_start
        }

    def add_event(self, heat_id, event):
        if heat_id in self.heats:
            self.heats[heat_id]["events"].append(event)
            if "position" in event:
                self.heats[heat_id]["position"] = event["position"]
            if "timestamp" in event:
                self.heats[heat_id]["last_update"] = event["timestamp"]

    def get_status(self, heat_id):
        return self.heats.get(heat_id, {}).get("status", "Unknown")

    def get_position(self, heat_id):
        return self.heats.get(heat_id, {}).get("position", None)

    def complete_heat(self, heat_id):
        if heat_id in self.heats:
            self.heats[heat_id]["status"] = "Completed"