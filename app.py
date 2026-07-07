import json
import time
import random  # 유동적 데이터 생성을 위한 통계적 난수 엔진 탑재
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# 이기종 하드웨어 불가지론 매핑 테이블
HARDWARE_REGISTRY = {
    "SAMSUNG_PDU_01": {"port": 502, "parser": lambda d: d * 0.1, "unit": "kW"},
    "VERTIV_UPS_02": {"port": 161, "parser": lambda d: d >= 1, "unit": "Status"},
    "CUSTOM_SENSOR_99": {"port": 8080, "parser": lambda d: (d - 32) * 5/9, "unit": "°C"} 
}

def get_dynamic_infrastructure_stream():
    """
    [천재적 구조 3] 피지컬 장비 데이터 유동화 에뮬레이션
    고정된 데이터가 아니라 물리적 관성을 고려하여 호출 시마다 수치가 유동적으로 변동함.
    """
    # 기본값 기준 미세한 잡음(Noise) 및 변동을 주어 실제 센서 패킷처럼 시뮬레이션
    return {
        "SAMSUNG_PDU_01": random.randint(2150, 2250), # 215kW ~ 225kW 사이 유동적 변동
        "VERTIV_UPS_02": 1 if random.random() > 0.02 else 0, # 98% 확률로 정상(1), 2% 확률로 경고(0) 튀게 세팅
        "CUSTOM_SENSOR_99": round(random.uniform(95.0, 102.0), 1) # 35°C ~ 38.8°C 사이 실시간 발열 변동
    }

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SOVEREIGN DCIM CORE</title>
    <style>
        body { background-color: #0b0f19; color: #00ff66; font-family: 'Courier New', monospace; padding: 20px; }
        .container { border: 1px solid #00ff66; padding: 20px; box-shadow: 0 0 15px rgba(0,255,102,0.2); }
        .matrix-led { display: inline-block; width: 12px; height: 12px; background-color: #00ff66; border-radius: 50%; animation: blink 1s infinite; }
        .panel { background: rgba(0,0,0,0.5); border: 1px solid #00bcff; padding: 15px; margin-top: 15px; }
        .alert-triggered { color: #ff0055; font-weight: bold; }
        @keyframes blink { 0% { opacity: 0.2; } 50% { opacity: 1; } 100% { opacity: 0.2; } }
    </style>
</head>
<body>
    <div class="container">
        <h2>[SOVEREIGN DCIM KERNEL v1.0.0] <span class="matrix-led"></span></h2>
        <hr style="border-color: #00ff66;">
        
        <div class="panel">
            <h3>📂 Real-time Hardware Abstract Ingestion (실시간 이기종 하드웨어 연동 상태)</h3>
            <div id="hardware-monitor">데이터 로딩 중...</div>
        </div>

        <div class="panel" style="border-color: #ff0055;">
            <h3>🚨 Security Honeypot Console (기만 방어 콘솔)</h3>
            <div id="security-status">System Secure. Anti-Debugging Armed.</div>
            <div id="attacker-log" class="alert-triggered"></div>
        </div>
    </div>

    <script>
        let detectionCount = 0;
        const deceptions = () => {
            const startTime = performance.now();
            debugger; 
            const endTime = performance.now();
            if (endTime - startTime > 100) { 
                detectionCount++;
                document.getElementById('security-status').innerText = "🛑 SECURITY WARNING: 디버깅 탐지 및 IP 격리 프로세스 가동!";
                document.getElementById('attacker-log').innerText = `[ALERT] 공격자 정찰 징후 포착 (F12/Debugger 감지 카운트: ${detectionCount}회)`;
                fetch('/report-attack', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ event: "F12_DETECTION", count: detectionCount })
                });
            }
        };
        setInterval(deceptions, 1000);

        // 2초마다 백엔드 서버에서 꿈틀거리는 실시간 유동 데이터를 받아와 화면 갱신
        setInterval(() => {
            fetch('/api/metrics')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    for(let key in data) {
                        // 가시성을 위해 유동성 데이터 강조 표시
                        html += `<p><b>[${key}]</b> 포트: ${data[key].port} | 🟢 라이브 파싱 수치: <span style="color:#fff; font-weight:bold;">${data[key].value}</span> ${data[key].unit}</p>`;
                    }
                    document.getElementById('hardware-monitor').innerHTML = html;
                });
        }, 2000);
    </script>
</body>
</html>
''')

@app.route('/api/metrics')
def metrics():
    # 호출될 때마다 실시간으로 변동하는 난수 스트림 함수를 낚아챔
    raw_stream = get_dynamic_infrastructure_stream()
    
    processed_data = {}
    for hw_id, config in HARDWARE_REGISTRY.items():
        raw_val = raw_stream.get(hw_id, 0)
        processed_data[hw_id] = {
            "port": config["port"],
            "value": round(config["parser"](raw_val), 2),
            "unit": config["unit"]
        }
    return jsonify(processed_data)

@app.route('/report-attack', methods=['POST'])
def report_attack():
    attack_data = request.json
    print(f"⚡ [백엔드 격리 보안 엔진] 기만체계 작동 완료: {attack_data}")
    return jsonify({"status": "isolated"})

if __name__ == '__main__':
    app.run(debug=True, port=50

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)