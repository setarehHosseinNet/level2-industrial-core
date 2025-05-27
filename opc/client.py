# فایل: opc/client.py
from opcua import Client

class OPCUAReader:
    def __init__(self, server_url):
        self.client = Client(server_url)

    def connect(self):
        self.client.connect()
        print("✅ Connected to OPC UA Server")

    def disconnect(self):
        self.client.disconnect()
        print("🔌 Disconnected from OPC UA Server")

    def read_node_value(self, node_id):
        node = self.client.get_node(node_id)
        return node.get_value()

    def read_multiple_nodes(self, node_ids):
        return {node_id: self.read_node_value(node_id) for node_id in node_ids}
