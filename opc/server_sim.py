# فایل: opc/server_sim.py
from opcua import Server
from datetime import datetime
import random
import time

# ایجاد سرور OPC UA
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# تعریف فضای نام
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# تعریف آبجکت اصلی
heat_obj = server.nodes.objects.add_object(idx, "HeatSimulation")
temp_node = heat_obj.add_variable(idx, "Temperature", 850.0)
status_node = heat_obj.add_variable(idx, "Status", "Active")
position_node = heat_obj.add_variable(idx, "Position", "LRF")

# فعال‌سازی قابلیت تغییر مقادیر
temp_node.set_writable()
status_node.set_writable()
position_node.set_writable()

# شروع سرور
server.start()
print("✅ OPC UA Server is running at opc.tcp://0.0.0.0:4840")

try:
    while True:
        # شبیه‌سازی تغییرات
        temp = round(random.uniform(840, 950), 2)
        temp_node.set_value(temp)
        print(f"🔥 Temperature updated: {temp}")

        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Stopping server...")
    server.stop()
