# app.py (실전 하드웨어 연동 PoC 프로토타입)
import asyncio
import random
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import google.generativeai as genai

app = FastAPI()

#==============================================================================
# [핵심] 실제 하드웨어 IoT 연동 및 AI 브레인 API 설정
#==============================================================================
GEMINI_API_KEY = "AQ.Ab8RN6LjEu1vpr6S7HXUWdmujsvMATBlOM4NhalhWYAVHf82sw"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 실제 하드웨어 통신을 가정한 인터페이스 객체 (PoC 수준)
class HardwareInterface:
    def read_telemetry(self, node_id):
        # 실제 환경에서는 이곳에 Modbus, SNMP, MQTT 드라이버 연동
        return {"temp": random.uniform(20, 28), "load": random.uniform(10, 450)}

hw = HardwareInterface()

#==============================================================================
# [프로토타입 로직]
#==============================================================================
@app.post("/command")
async def process_request(request: Request):
    data = await request.json()
    user_query = data.get("query")
    
    # AI에게 현장 상황과 하드웨어 데이터를 전송하여 판단 요청
    prompt = f"""
    당신은 dcim.kr 소버린 AI 커널임.
    현재 하드웨어 상태: {hw.read_telemetry('NODE_04')}
    사용자 지시: {user_query}
    지시를 수행하고, 기술적인 인프라 분석 보고서를 명사형 어조로 출력하라.
    """
    
    response = model.generate_content(prompt)
    
    return {"status": "success", "ai_analysis": response.text, "timestamp": datetime.datetime.now().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-950 text-white p-8">
        <h1 class="text-3xl font-bold mb-6 text-cyan-400">dcim.kr 하드웨어 연동 프로토타입</h1>
        <div class="grid grid-cols-2 gap-8">
            <div class="border border-slate-700 p-6 rounded-xl">
                <h2 class="text-xl mb-4">현장 하드웨어 제어 인터페이스</h2>
                <input id="cmd" class="w-full bg-slate-900 p-3 rounded mb-4" placeholder="지시사항을 입력하세요 (예: 노드4 온도 상승 대응)">
                <button onclick="send()" class="bg-cyan-600 px-6 py-2 rounded">명령 전송</button>
            </div>
            <div id="result" class="border border-slate-700 p-6 rounded-xl overflow-y-auto h-96">
                인프라 분석 결과가 여기에 출력됩니다...
            </div>
        </div>
        <script>
            async function send() {
                const query = document.getElementById('cmd').value;
                const res = await fetch('/command', {method: 'POST', body: JSON.stringify({query}), headers: {'Content-Type': 'application/json'}});
                const data = await res.json();
                document.getElementById('result').innerHTML = `<pre class="whitespace-pre-wrap text-sm">${data.ai_analysis}</pre>`;
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)