# فایل: test_opc_client.py
from opc.client import OPCUAReader

# آدرس سرور شبیه‌سازی‌شده ما
SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"

# ساخت کلاینت و اتصال
opc_reader = OPCUAReader(SERVER_URL)
opc_reader.connect()

# خواندن داده‌ها از سه نود اصلی
node_ids = [
    "ns=2;s=HeatSimulation.Temperature",
    "ns=2;s=HeatSimulation.Status",
    "ns=2;s=HeatSimulation.Position"
]

# چاپ داده‌های خوانده‌شده
values = opc_reader.read_multiple_nodes(node_ids)
for node, val in values.items():
    print(f"{node} -> {val}")

opc_reader.disconnect()
