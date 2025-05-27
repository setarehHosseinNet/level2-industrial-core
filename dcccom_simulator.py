# فایل: dcccom_simulator.py
import time
import random
import json

class DCCCOMSimulator:
    def __init__(self):
        self.available_tags = {
            "WinCC.Tag.Temperature": lambda: round(random.uniform(850, 950), 2),
            "WinCC.Tag.Status": lambda: random.choice(["Active", "Idle", "Alarm"]),
            "WinCC.Tag.Position": lambda: random.choice(["LRF", "CCM", "RH", "Ladle Park"])
        }

    def read_tag(self, tag_name):
        if tag_name in self.available_tags:
            return self.available_tags[tag_name]()
        else:
            raise ValueError(f"Tag '{tag_name}' not found")

    def read_all(self):
        return {tag: gen() for tag, gen in self.available_tags.items()}

    def simulate_stream(self, interval=5):
        print("🔁 DCCCOM Simulation Started...")
        try:
            while True:
                data = self.read_all()
                print(json.dumps(data, indent=2))
                time.sleep(interval)
        except KeyboardInterrupt:
            print("⛔ DCCCOM Simulation Stopped")

if __name__ == "__main__":
    sim = DCCCOMSimulator()
    sim.simulate_stream()
