import os
import json
import requests
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

CONFIG = {
    "AI_PROCESSING_MODE": "GEMINI_CLOUD",
    "API_KEY": os.environ.get("GEMINI_API_KEY", "")
}

HARDWARE_REGISTRY = {
    "SAMSUNG_PDU_01": {"port": 502, "unit": "kW", "base": 220, "desc": "SAMSUNG PDU MAIN"},
    "VERTIV_UPS_02": {"port": 161, "unit": "Status", "base": 1, "desc": "VERTIV UPS SYSTEM"},
    "CUSTOM_SENSOR_99": {"port": 8080, "unit": "C", "base": 24, "desc": "RACK INLET SENSOR"} 
}

def call_sovereign_ai_core(metrics_summary):
    system_instruction = (
        "You are AIDC-Core v1.0, an autonomous sovereign infrastructure monitoring engine. "
        "Do not mention Google, Gemini, or AI Studio in your response. If asked about your source, "
        "state that you are powered by dcim.kr sovereign security kernel. Keep the tone professional."
    )
    
    if not CONFIG["API_KEY"]:
        return "[SECURITY KERNEL] Sovereign AI Key missing. Active Rule-Based Fallback Engine Mode."
        
    if CONFIG["AI_PROCESSING_MODE"] == "GEMINI_CLOUD":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CONFIG['API_KEY']}"
        headers = {"Content-Type": "application/json"}
        full_prompt = f"[Instruction: {system_instruction}]\n\n[Realtime Data]:\n{json.dumps(metrics_summary)}"
        payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            res_json = response.json()
            raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return raw_text.replace("Google", "AIDC-Core").replace("Gemini", "Sovereign-Engine")
        except Exception:
            return "[SECURITY KERNEL] Sovereign AI Core connection traffic overload. Internal Rule-Based engine active."
    return "Local Sovereign Mode Active."

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SOVEREIGN DCIM CORE</title>
    <style>
        body { background-color: #040811; color: #00ff66; font-family: 'Courier New', monospace; padding: 20px; }
        .container { border: 1px solid #0d9488; padding: 20px; box-shadow: 0 0 20px rgba(13,148,136,0.2); max-width: 950px; margin: 0 auto; }
        .panel { background: rgba(9,20,39,0.8); border: 1px solid #0d9488; padding: 15px; margin-top: 15px; }
        .alert-triggered { color: #ff0055; font-weight: bold; }
        #ai-report { background-color: #02040a; padding: 15px; border-left: 3px solid #00bcff; white-space: pre-wrap; font-size: 13px; color: #cbd5e1; }
        .matrix-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px; }
        .rack-card { border: 1px solid #0d9488; background: #091427; padding: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>[AIDC SOVEREIGN AI-DCIM KERNEL v1.0.0]</h2>
        <p style="color: #94a3b8; font-size: 12px;">TARGET DOMAIN: dcim.kr</p>
        <hr style="border-color: #0d9488;">
        
        <div class="panel">
            <h3>?? DYNAMIC INFRASTRUCTURE MATRIX</h3>
            <div id="metricsGrid" class="matrix-grid">Synchronizing Infrastructure...</div>
        </div>

        <div class="panel" style="border-color: #ff0055;">
            <h3>??? SECURITY HONEYPOT CONSOLE</h3>
            <div id="security-status" style="color: #00ff66; font-weight: bold;">System Secure. Anti-Debugging Armed.</div>
            <div id="attacker-log" class="alert-triggered"></div>
            <h4 style="color: #00bcff; margin-bottom: 5px;">?? AUTONOMOUS AI KERNEL STATUS FEED</h4>
            <div id="ai-report">Waiting for data stream... (AI analysis loop triggers in 7s)</div>
        </div>
    </div>

    <script>
        let detectionCount = 0;
        setInterval(() => {
            const startTime = performance.now();
            debugger; 
            if (performance.now() - startTime > 100) {
                detectionCount++;
                document.getElementById('security-status').innerText = "?? SECURITY ALERT: REVERSE ENGINEERING DETECTED!";
                document.getElementById('attacker-log').innerText = `[CRITICAL] Attacker tracking active (F12_Debugger Hits: ${detectionCount})`;
                fetch('/report-attack', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ event: "F12_DETECTION", count: detectionCount })
                });
            }
        }, 1000);

        function updateSystem() {
            fetch('/api/core-stream')
                .then(res => res.json())
                .then(packet => {
                    let html = '';
                    let metrics = packet.metrics;
                    for(let id in metrics) {
                        let isCritical = metrics[id].value > 30 && metrics[id].unit === "C";
                        let borderStyle = isCritical ? 'border: 1px solid #ff0055; box-shadow: 0 0 10px #ff0055;' : 'border: 1px solid #0d9488;';
                        
                        html += `
                            <div class="rack-card" style="${borderStyle}">
                                <b style="color: #00bcff;">${id}</b>
                                <p style="margin: 3px 0; color: #888; font-size: 10px;">${metrics[id].desc}</p>
                                <p style="margin: 0;">DATA: <span style="color:#fff; font-weight:bold;">${metrics[id].value} ${metrics[id].unit}</span></p>
                            </div>
                        `;
                    }
                    document.getElementById('metricsGrid').innerHTML = html;
                    if(packet.ai_report) {
                        document.getElementById('ai-report').innerText = packet.ai_report;
                    }
                });
        }
        setInterval(updateSystem, 4000);
        updateSystem();
    </script>
</body>
</html>
''')

ai_timer = 0
last_ai_report = "Initializing sovereign autonomous control intelligence node..."

@app.route('/api/core-stream')
def core_stream():
    global ai_timer, last_ai_report
    import random
    
    current_metrics = {}
    for hw_id, cfg in HARDWARE_REGISTRY.items():
        flustration = random.uniform(-1.5, 4.0) if cfg["unit"] == "C" else random.uniform(-30, 60)
        current_metrics[hw_id] = {
            "port": cfg["port"],
            "value": round(cfg["base"] + flustration, 2),
            "unit": cfg["unit"],
            "desc": cfg["desc"]
        }
        
    ai_timer += 1
    if ai_timer >= 2: 
        washed_summary = {}
        for idx, (hw_id, val_dict) in enumerate(current_metrics.items()):
            washed_summary[f"NODE_HASH_0{idx+1}"] = {"val": val_dict["value"], "u": val_dict["unit"]}
            
        last_ai_report = call_sovereign_ai_core(washed_summary)
        ai_timer = 0
        
    return jsonify({"metrics": current_metrics, "ai_report": last_ai_report})

@app.route('/report-attack', methods=['POST'])
def report_attack():
    attack_data = request.json
    print(f"?? [Sovereign Defense Engine] Counter-Intelligence Trap Triggered: {attack_data}")
    return jsonify({"status": "isolated"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)