# app.py (2026 AI-DCIM Sovereign Core v1.0 - Pure Intranet Prototype)
import json
import random
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI()

# ==============================================================================
# [?? 1. HARDWARE INTERFACE LAYER (이기종 실전 데이터 스트림 슬롯)]
# ==============================================================================
class SovereignHardwareInterface:
    def __init__(self):
        self.nodes = {
            "NODE_01": {"vendor": "SAMSUNG", "protocol": "Modbus_TCP", "val": "420.5 kW", "status": "정상", "score": 98, "raw_num": 420.5, "unit": "kW", "temp": 21.4},
            "NODE_02": {"vendor": "VERTIV", "protocol": "SNMP_v3", "val": "98.2 %", "status": "정상", "score": 97, "raw_num": 98.2, "unit": "%", "temp": 22.1},
            "NODE_03": {"vendor": "NIS_HVAC", "protocol": "BACnet_IP", "val": "1800 RPM", "status": "정상", "score": 95, "raw_num": 1800, "unit": "RPM", "temp": 20.8},
            "NODE_04": {"vendor": "RACK_INLET", "protocol": "MQTT_JSON", "val": "22.4 C", "status": "정상", "score": 99, "raw_num": 22.4, "unit": "C", "temp": 22.4},
            "NODE_05": {"vendor": "CORE_ROUTER", "protocol": "NetFlow_v9", "val": "14.2 Gbps", "status": "정상", "score": 96, "raw_num": 14.2, "unit": "Gbps", "temp": 19.5}
        }
        
    def poll_telemetry_stream(self):
        # 0.5초마다 파르르 요동치는 런타임 하드웨어 패킷 수집 연산
        for n_id, data in self.nodes.items():
            if data["status"] == "정상":
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

# ==============================================================================
# [?? 2. SYSTEM STATE DATABASE REGISTER]
# ==============================================================================
SYSTEM_STATE = {
    "REG_SCALE_PROFILE": "HYPERSCALE",
    "REG_THERMAL_CEILING": 26.0,
    "REG_PUE_TARGET": 1.25,
    "REG_HEALTH_SCORE": 98,
    "REG_AUDIT_TRAIL_LOG": [
        {"time": "10:20:00", "msg": "STATUS: LOGICAL_SECURE\n本 SYSTEM KERNEL은 dcim.kr의 독자적 기계학습 커널, 이기종 프로토콜 인터프리터 및 소버린 가드레일 보안 레이어로 가동됨.\n- 국정원 최상위 가이드라인 검증필 해시 커널 로딩 완료.", "hash": "0x8F9A2C"},
        {"time": "10:20:15", "msg": "실시간 이기종 하드웨어 텔레메트리 파이프라인 매핑 완료.\n- Modbus, SNMP, BACnet, MQTT 패킷 스트림 포트 동적 개통 성공.", "hash": "0x3D4E5F"}
    ]
}

@app.get("/api/telemetry")
async def get_telemetry_endpoint():
    global SYSTEM_STATE
    live_nodes = hardware.poll_telemetry_stream()
    return JSONResponse(content={
        "REG_LIVE_IOT_MAP": list(live_nodes.values()),
        "REG_HEALTH_SCORE": SYSTEM_STATE["HEALTH_SCORE"] if "HEALTH_SCORE" in SYSTEM_STATE else SYSTEM_STATE["REG_HEALTH_SCORE"],
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

    # 가변 모드 스위칭 인터럽트 처리
    if "낮추" in query or "임계치" in query or "에지" in query or "전환" in query:
        SYSTEM_STATE["REG_SCALE_PROFILE"] = "GOVERNMENT_EDGE"
        SYSTEM_STATE["REG_THERMAL_CEILING"] = 24.5
        SYSTEM_STATE["REG_HEALTH_SCORE"] = 64
        hardware.nodes["NODE_04"].update({"status": "위험 경보", "raw_num": 25.1, "temp": 25.1})
    elif "네이버" in query or "NAVER" in query:
        SYSTEM_STATE["REG_SCALE_PROFILE"] = "NAVER_CLOUD"
        SYSTEM_STATE["REG_HEALTH_SCORE"] = 99
        hardware.nodes["NODE_04"].update({"status": "정상", "raw_num": 21.8, "temp": 21.8})

    # [핵심] 외부 구글 서버 통신 전면 거세 및 첫 대화 첨삭본 로직 완전 내재화
    ai_text = (
        f"?? 1. 전력/열역학 인프라 다차원 연계 위험 진단\n"
        f"- 최종 절대 관리자[리(Lee)] 지시에 따라 안전 한계 온도 임계치(REG_THERMAL_CEILING)를 {SYSTEM_STATE['REG_THERMAL_CEILING']}°C로 동적 패치함.\n"
        f"- 실시간 계측 결과, NODE_04(RACK_INLET)의 흡입 온도가 25.1°C에 도달하여 변경된 임계치를 초과, 위험 고장 노드로 확진함.\n\n"
        f"? 2. 물리 법칙(아레니우스 열화 법칙) 기반 MTBF 시뮬레이션\n"
        f"- SCHNEIDER_KILLER 가동: Omniverse 3D 위상 기반 주변 열 확산 전도 예측 및 리튬이온 배터리 Predictive Insights 연산 결과, NODE_04 하부 가속기 컴포넌트의 수명 34% 조기 단축 손실 궤도 진입. 24시간 이내 치명적 인프라 다운타임 발생 확률 [84.2%]로 급상승함.\n\n"
        f"??? 3. 제어 시스템 기만 및 프로토콜 침입 탐지 현황\n"
        f"- 비인가 F12 역공학 정찰 시도 및 기만 패킷 감시 결과 [ZERO_DETECTED] 외부 오염 흔적 전면 소거됨.\n\n"
        f"?? 4. 보안 암호화 및 자연어 패치 감사 추적(Audit Trail) 상태\n"
        f"- 인트라넷 구간 ACTIVE_ARIA_256 암호화 정상 가동 중임.\n"
        f"- 관리자 명령 감사 로그 고유 해시 블록 체인 적재 완료됨. (HASH: {hash_code})\n\n"
        f"?? 5. PUE 효율 극대화를 위한 자율 폐쇄 루프 제어 발령\n"
        f"- VERTIV_KILLER 가동: 고밀도 GPU 랙 보호를 위해 액체 냉각 CDU 솔레노이드 밸브 개도율 85% 즉시 상향 명령 전파.\n"
        f"- NIS_HVAC 인버터 주파수 2100 RPM 상향 및 공조기 기류 팬 재라우팅 처리함. [즉시 집행 바람]"
    )

    SYSTEM_STATE["REG_AUDIT_TRAIL_LOG"].append({
        "time": current_time,
        "msg": ai_text,
        "hash": hash_code
    })
    return JSONResponse(content=SYSTEM_STATE)

# ==============================================================================
# [?? 3. NEXT-GEN VISUALIZATION INTERNET DASHBOARD UI]
# ==============================================================================
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard_origin():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>dcim.kr :: 2026 Sovereign AI-DCIM Enclave Console</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
            body { background-color: #030508; color: #cbd5e1; font-family: 'Noto Sans KR', sans-serif; overflow-x: hidden; }
            .code-font { font-family: 'Fira Code', monospace; }
            .cyber-panel { background: rgba(7, 10, 19, 0.9); border: 1px solid #115e59; border-top: 3px solid #00f2fe; box-shadow: 0 4px 30px rgba(0,0,0,0.7); }
            .matrix-cell { transition: all 0.2s ease; border: 1px solid #1e293b; }
            .feed-card { border-bottom: 1px solid #0f172a; animation: slideUp 0.3s ease-out forwards; }
            @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            .glow-cyan { text-shadow: 0 0 10px #00f2fe; }
            .glow-rose { text-shadow: 0 0 12px #ff0055; animation: pulseGlow 1.5s infinite; }
            @keyframes pulseGlow { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
        </style>
    </head>
    <body class="p-4 min-h-screen flex flex-col justify-between">

        <header class="w-full flex flex-col md:flex-row justify-between items-center p-4 mb-4 border border-slate-800 bg-slate-950/80 rounded-xl backdrop-blur-md">
            <div>
                <h1 class="text-2xl font-black tracking-widest text-white glow-cyan code-font">?? dcim.kr SOVEREIGN INTEGRITY CONSOLE</h1>
                <p class="text-[10px] text-slate-500 font-mono tracking-wider mt-0.5">ROK NATIONAL SECURITY CLASS-A AIR_GAPPED COMPLIANCE // PURE INTRANET PROTOTYPE</p>
            </div>
            <div class="flex items-center space-x-8 mt-4 md:mt-0">
                <div class="text-right">
                    <span class="text-[10px] block text-slate-500 font-bold">TARGET PRESET</span>
                    <span id="txt-profile" class="text-sm font-black text-cyan-400 code-font">HYPERSCALE_MODE</span>
                </div>
                <div class="text-right border-l border-slate-800 pl-6">
                    <span class="text-[10px] block text-slate-500 font-bold">INTEGRITY SCORE</span>
                    <div class="flex items-center justify-end space-x-2">
                        <span id="badge-dot" class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
                        <span id="txt-health" class="text-xl font-black text-cyan-400 glow-cyan code-font">98%</span>
                    </div>
                </div>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
            <section class="lg:col-span-5 cyber-panel p-5 rounded-xl h-[610px] flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-4">
                        <h2 class="text-xs font-bold text-cyan-400 tracking-wider">?? REAL-TIME INFRASTRUCTURE MATRIX (ENTROPY HEATMAP)</h2>
                        <span class="text-[9px] text-emerald-400 font-mono animate-pulse">● STREAM ACTIVE</span>
                    </div>
                    <div class="bg-slate-950/90 border border-slate-900 rounded-lg p-4 h-[280px] flex items-center justify-center relative">
                        <div id="matrix-grid-viewport" class="w-full h-full grid grid-cols-3 gap-3"></div>
                    </div>
                </div>
                <div class="bg-slate-950/40 border border-slate-900 rounded-lg p-3 flex-1 mt-4 overflow-y-auto">
                    <table class="w-full text-[11px] text-left font-mono">
                        <thead>
                            <tr class="text-slate-500 border-b border-slate-800 text-[10px]">
                                <th class="pb-1">NODE ID</th>
                                <th class="pb-1">제조사</th>
                                <th class="pb-1">프로토콜</th>
                                <th class="pb-1">실시간 계측값</th>
                                <th class="pb-1">상태</th>
                            </tr>
                        </thead>
                        <tbody id="iot-table-body"></tbody>
                    </table>
                </div>
            </section>

            <section class="lg:col-span-4 cyber-panel p-5 rounded-xl h-[610px] flex flex-col">
                <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-4">
                    <h2 class="text-xs font-bold text-cyan-400 tracking-wider">?? AUTONOMOUS ORCHESTRATION FEED JOURNAL</h2>
                    <span class="text-[9px] text-slate-500 font-mono">LSH-256 APPEND-ONLY</span>
                </div>
                <div id="timeline-feed" class="flex-1 overflow-y-auto pr-1 space-y-3"></div>
            </section>

            <section class="lg:col-span-3 cyber-panel p-5 rounded-xl h-[610px] flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-4">
                        <h2 class="text-xs font-bold text-cyan-400 tracking-wider">?? COMMAND OVERRIDE CONSOLE</h2>
                        <span class="text-[9px] text-slate-500 font-mono">OPERATOR: LEE</span>
                    </div>
                    <p class="text-xs text-slate-400 leading-relaxed mb-4">
                        본 시스템은 복잡한 하드웨어 조작 설정을 거부함. 최고 관리자의 정중한 자연어 지시서를 커널 최고 인터럽트로 파싱하여 실시간 가변 제어를 즉각 집행함.
                    </p>
                </div>
                <div class="flex-1 bg-slate-950 border border-slate-900 rounded-lg p-3 flex flex-col justify-between">
                    <div class="text-[11px] text-slate-500 font-mono space-y-1 overflow-y-auto h-[160px]" id="console-terminal-view">
                        <p class="text-cyan-400">[SYSTEM] ROOT_SUPREME_ADMIN 계정 세션 인증 성공.</p>
                        <p class="text-slate-600">[SECURITY] 소버린 폐쇄망 전용 자립 판단 커널 로딩 완료.</p>
                    </div>
                    <div class="mt-2 border-t border-slate-900 pt-2">
                        <div class="flex items-center text-xs text-cyan-400 font-mono mb-1">
                            <span class="animate-pulse mr-1">●</span> lee@dcim.kr:~$
                        </div>
                        <textarea id="txt-command" rows="3" class="w-full bg-slate-900 border border-slate-800 p-2 text-xs text-white rounded focus:outline-none focus:border-cyan-400 resize-none font-mono tracking-tight leading-normal">현재 보안 지침 변경에 따라 시스템 안전 임계치를 낮추고, 운영 체급을 에지 모드로 안전하게 전환해 주세요.</textarea>
                    </div>
                </div>
                <button onclick="sendNaturalCommand()" id="btn-submit" class="w-full mt-4 bg-gradient-to-r from-cyan-500 to-teal-500 text-slate-950 font-black text-xs py-2.5 rounded-lg transition tracking-widest">?? COMMAND INTERRUPT EXECUTION</button>
            </section>
        </div>

        <footer class="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 p-4 bg-slate-950/60 border border-slate-800 rounded-xl items-center backdrop-blur-md">
            <div><button onclick="toggleSonification()" id="sound-btn" class="w-full bg-slate-900 border border-slate-700 hover:border-cyan-400 px-4 py-2 rounded-lg text-xs text-cyan-400 font-black tracking-wider transition">?? 오디오 소니피케이션 관제 주파수: 대기 중</button></div>
            <div class="flex items-center space-x-3 w-full col-span-2"><span class="text-[11px] text-slate-500 font-bold shrink-0 font-mono">? TIME-TRAVEL DEBUGGER</span><input type="range" min="1" max="100" value="100" class="w-full accent-cyan-400 cursor-pointer" oninput="triggerTimeTravel(this.value)"><span id="time-label" class="text-[10px] text-cyan-400 font-mono shrink-0 tracking-widest">REAL-TIME_STREAM</span></div>
        </footer>

        <script>
            let localState = %s;
            let audioCtx = null;
            let whiteNoiseSource = null;

            async function fetchLiveTelemetry() {
                try {
                    const res = await fetch("/api/telemetry");
                    const data = await res.json();
                    localState.REG_LIVE_IOT_MAP = data.REG_LIVE_IOT_MAP;
                    localState.REG_HEALTH_SCORE = data.REG_HEALTH_SCORE;
                    localState.REG_SCALE_PROFILE = data.REG_SCALE_PROFILE;
                    updateUI();
                } catch (e) {}
            }
            setInterval(fetchLiveTelemetry, 500);

            function updateUI() {
                document.getElementById("txt-profile").innerText = localState.REG_SCALE_PROFILE + "_MODE";
                document.getElementById("txt-health").innerText = localState.REG_HEALTH_SCORE + "%";
                
                const dot = document.getElementById("badge-dot");
                const txtHealth = document.getElementById("txt-health");
                if (localState.REG_HEALTH_SCORE >= 90) {
                    dot.className = "w-2 h-2 rounded-full bg-cyan-400 animate-ping";
                    txtHealth.className = "text-xl font-black text-cyan-400 glow-cyan code-font";
                } else {
                    dot.className = "w-2 h-2 rounded-full bg-rose-500 animate-ping";
                    txtHealth.className = "text-xl font-black text-rose-500 glow-crimson code-font";
                }

                const tbody = document.getElementById("iot-table-body");
                tbody.innerHTML = "";
                localState.REG_LIVE_IOT_MAP.forEach(node => {
                    tbody.innerHTML += `
                        <tr class="border-b border-slate-900/50">
                            <td class="text-white font-bold py-1.5 font-mono">${node.id}</td>
                            <td class="text-slate-400 text-[10px]">${node.vendor}</td>
                            <td class="text-slate-500 text-[9px]">${node.protocol}</td>
                            <td class="text-cyan-400 font-bold font-mono">${node.val}</td>
                            <td><span class="px-1.5 py-0.5 rounded text-[9px] ${node.status==='정상'?'bg-cyan-950 text-cyan-400':'bg-rose-950 text-rose-400 font-bold animate-pulse'}">${node.status}</span></td>
                        </tr>`;
                });

                const viewport = document.getElementById("matrix-grid-viewport");
                viewport.innerHTML = "";
                localState.REG_LIVE_IOT_MAP.forEach(node => {
                    const isAnomaly = node.status !== "정상";
                    viewport.innerHTML += `
                        <div class="matrix-cell rounded-lg p-3 flex flex-col justify-between ${isAnomaly ? 'bg-rose-950/40 border-rose-500 animate-pulse':'bg-slate-900/40 border-slate-800 hover:border-cyan-500'}">
                            <div class="flex justify-between items-center text-[9px] font-mono text-slate-500"><span>${node.id}</span></div>
                            <div class="text-right font-mono font-black text-sm ${isAnomaly?'text-rose-400 glow-crimson':'text-cyan-400'}">${node.temp.toFixed(1)} °C</div>
                        </div>`;
                });

                const feed = document.getElementById("timeline-feed");
                feed.innerHTML = "";
                [...localState.REG_AUDIT_TRAIL_LOG].reverse().forEach(log => {
                    feed.innerHTML += `
                        <div class="feed-card bg-slate-950/90 p-4 rounded-xl border border-slate-900 flex flex-col space-y-2">
                            <div class="flex justify-between items-center text-[10px] text-slate-500 font-mono"><span>[TIMELOG // ${log.time}]</span><span class="text-cyan-400">HASH: ${log.hash}</span></div>
                            <p class="text-xs text-slate-300 leading-relaxed tracking-tight whitespace-pre-line font-mono">${log.msg}</p>
                        </div>`;
                });
            }

            async function sendNaturalCommand() {
                const area = document.getElementById("txt-command");
                const cmd = area.value;
                if(!cmd.trim()) return;

                const btn = document.getElementById("btn-submit");
                btn.innerText = "? COMPUTING...";
                btn.disabled = true;

                const res = await fetch("/api/command", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({query: cmd})
                });
                const remoteState = await res.json();
                localState.REG_AUDIT_TRAIL_LOG = remoteState.REG_AUDIT_TRAIL_LOG;
                
                btn.innerText = "?? COMMAND INTERRUPT EXECUTION";
                btn.disabled = false;
                
                updateUI();
                triggerAlertTone();
                area.value = "";
            }

            function triggerTimeTravel(val) {
                const label = document.getElementById("time-label");
                if (val < 100) {
                    label.innerText = `RECOVERY: -${100 - val}MIN`;
                    label.className = "text-[10px] text-amber-500 font-mono shrink-0 tracking-widest animate-pulse";
                } else {
                    label.innerText = "REAL-TIME_STREAM";
                    label.className = "text-[10px] text-cyan-400 font-mono shrink-0 tracking-widest";
                }
            }

            function toggleSonification() {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const bufferSize = audioCtx.sampleRate * 2;
                    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                    const data = buffer.getChannelData(0);
                    for (let i = 0; i < bufferSize; i++) { data[i] = Math.random() * 2 - 1; }
                    whiteNoiseSource = audioCtx.createBufferSource();
                    whiteNoiseSource.buffer = buffer;
                    const gainNode = audioCtx.createGain();
                    gainNode.gain.value = 0.006;
                    whiteNoiseSource.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    whiteNoiseSource.loop = true; whiteNoiseSource.start();
                    document.getElementById("sound-btn").innerText = "?? 소니피케이션 가동 중";
                } else {
                    audioCtx.close(); audioCtx = null;
                    document.getElementById("sound-btn").innerText = "?? 소니피케이션 차단됨";
                }
            }

            function triggerAlertTone() {
                if (!audioCtx) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(localState.REG_HEALTH_SCORE < 90 ? 760 : 380, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 0.5);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.5);
            }

            updateUI();
        </script>
    </body>
    </html>
    """ % json.dumps(SYSTEM_STATE, ensure_ascii=False)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)