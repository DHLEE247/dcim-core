# app.py (2026 AI-DCIM Sovereign Core v1.0 - UTF-8 Free Safe Prototype)
import json
import random
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SovereignHardwareInterface:
    def __init__(self):
        self.nodes = {
            "NODE_01": {"id": "NODE_01", "vendor": "SAMSUNG", "protocol": "Modbus_TCP", "val": "420.5 kW", "status": "NORMAL", "score": 98, "raw_num": 420.5, "unit": "kW", "temp": 21.4},
            "NODE_02": {"id": "NODE_02", "vendor": "VERTIV", "protocol": "SNMP_v3", "val": "98.2 %", "status": "NORMAL", "score": 97, "raw_num": 98.2, "unit": "%", "temp": 22.1},
            "NODE_03": {"id": "NODE_03", "vendor": "NIS_HVAC", "protocol": "BACnet_IP", "val": "1800 RPM", "status": "NORMAL", "score": 95, "raw_num": 1800, "unit": "RPM", "temp": 20.8},
            "NODE_04": {"id": "NODE_04", "vendor": "RACK_INLET", "protocol": "MQTT_JSON", "val": "22.4 C", "status": "NORMAL", "score": 99, "raw_num": 22.4, "unit": "C", "temp": 22.4},
            "NODE_05": {"id": "NODE_05", "vendor": "CORE_ROUTER", "protocol": "NetFlow_v9", "val": "14.2 Gbps", "status": "NORMAL", "score": 96, "raw_num": 14.2, "unit": "Gbps", "temp": 19.5}
        }
        
    def poll_telemetry_stream(self):
        for n_id, data in self.nodes.items():
            if data["status"] == "NORMAL" or data["status"] == "AI_CONTROL":
                if data["unit"] == "kW": data["raw_num"] += random.uniform(-1.2, 1.2)
                elif data["unit"] == "%": data["raw_num"] += random.uniform(-0.05, 0.05)
                elif data["unit"] == "RPM": data["raw_num"] += random.uniform(-4, 4)
                elif data["unit"] == "C": 
                    data["raw_num"] += random.uniform(-0.08, 0.08)
                    data["temp"] = data["raw_num"]
                elif data["unit"] == "Gbps": data["raw_num"] += random.uniform(-0.03, 0.03)
                data["score"] = random.randint(96, 99)
            else:
                data["raw_num"] += random.uniform(-0.2, 0.2)
                data["temp"] = data["raw_num"]
                data["score"] = random.randint(48, 54)
            data["val"] = f"{data['raw_num']:.1f} {data['unit']}"
        return self.nodes

hardware = SovereignHardwareInterface()

SYSTEM_STATE = {
    "REG_SCALE_PROFILE": "HYPERSCALE",
    "REG_THERMAL_CEILING": 26.0,
    "REG_PUE_TARGET": 1.25,
    "REG_HEALTH_SCORE": 98,
    "REG_AUDIT_TRAIL_LOG": [
        {"time": "10:20:00", "msg": "STATUS: LOGICAL_SECURE / AIDC Core Kernel Loaded Successfully.", "hash": "0x8F9A2C"},
        {"time": "10:20:15", "msg": "Telemetry streaming established. Protocol adapters active.", "hash": "0x3D4E5F"}
    ]
}

@app.get("/api/telemetry")
async def get_telemetry_endpoint():
    global SYSTEM_STATE
    live_nodes = hardware.poll_telemetry_stream()
    return JSONResponse(content={
        "REG_LIVE_IOT_MAP": list(live_nodes.values()),
        "REG_HEALTH_SCORE": SYSTEM_STATE["REG_HEALTH_SCORE"],
        "REG_SCALE_PROFILE": SYSTEM_STATE["REG_SCALE_PROFILE"],
        "REG_THERMAL_CEILING": SYSTEM_STATE["REG_THERMAL_CEILING"]
    })

@app.post("/api/command")
async def execute_sovereign_command(payload: Request):
    global SYSTEM_STATE
    body = await payload.json()
    query = body.get("query", "")
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hash_code = f"0x{hex(hash(query) & 0xffffff)[2:].upper()}"

    if "낮추" in query or "임계치" in query or "에지" in query or "전환" in query:
        SYSTEM_STATE["REG_SCALE_PROFILE"] = "GOVERNMENT_EDGE"
        SYSTEM_STATE["REG_THERMAL_CEILING"] = 24.5
        SYSTEM_STATE["REG_HEALTH_SCORE"] = 64
        hardware.nodes["NODE_04"].update({"status": "CRITICAL", "raw_num": 25.1, "temp": 25.1})
        ai_text = "Analysis: NODE_04 Inlet temperature exceeded limit 24.5C. MTBF simulation drops by 34%. Closed-loop action triggered: Vertiv liquid cooling solenoid valve expanded to 85%."
    elif "네이버" in query or "NAVER" in query:
        SYSTEM_STATE["REG_SCALE_PROFILE"] = "NAVER_CLOUD"
        SYSTEM_STATE["REG_HEALTH_SCORE"] = 99
        hardware.nodes["NODE_04"].update({"status": "NORMAL", "raw_num": 21.8, "temp": 21.8})
        ai_text = "Analysis: Switched to Naver Cloud 12x12 telemetry profile. Zero-shot infrastructure data mapped safely."
    else:
        ai_text = "Analysis: Core system operational. All nodes secured within PUE margins."

    SYSTEM_STATE["REG_AUDIT_TRAIL_LOG"].append({
        "time": current_time,
        "msg": ai_text,
        "hash": hash_code
    })
    return JSONResponse(content=SYSTEM_STATE)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)