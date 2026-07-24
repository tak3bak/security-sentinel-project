import json
import time
import os

LOG_FILE_PATH = "custom_network_scan.json"

def generate_logs():
    endpoints = [
        {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "integration": "deep_network_scan",
            "device_ip": "10.0.0.1",
            "device_name": "XFINITY",
            "device_type": "IoT Device",
            "ports_open": [80, 443, 1883],
            "suspicious": True,
            "security_issue": "MQTT broker open without TLS — IoT device commands interceptable",
            "severity": "MEDIUM"
        },
        {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "integration": "deep_network_scan",
            "device_ip": "10.0.0.34",
            "device_name": "D32h-J04-b45b34c19c7bea405ca277...",
            "device_type": "Smart TV / Streamer",
            "ports_open": [7000, 8443],
            "suspicious": False
        },
        {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "integration": "deep_network_scan",
            "device_ip": "10.0.0.135",
            "device_type": "Unidentified device",
            "suspicious": False
        },
        {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "integration": "deep_network_scan",
            "device_ip": "10.0.0.231",
            "device_type": "Unidentified device",
            "suspicious": False
        },
        {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "integration": "deep_network_scan",
            "device_ip": "10.0.0.232",
            "device_type": "Unidentified device",
            "suspicious": False
        }
    ]

    with open(LOG_FILE_PATH, "a") as f:
        for endpoint in endpoints:
            f.write(json.dumps(endpoint) + "\n")

    print(f"Scan logs successfully written to {LOG_FILE_PATH}")

if __name__ == "__main__":
    generate_logs()
