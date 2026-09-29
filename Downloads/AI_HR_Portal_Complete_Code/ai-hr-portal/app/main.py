from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from .rag import answer_question

app = FastAPI(title="AI HR Portal", version="1.0.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1500)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse("""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI HR Portal</title><style>
body{font-family:Arial,sans-serif;background:#f2f5fa;margin:0;color:#1b2b43}
header{background:#17365d;color:white;padding:22px 7%}main{max-width:850px;margin:34px auto;padding:0 18px}
.card{background:white;border-radius:14px;padding:26px;box-shadow:0 8px 28px #18365d18}
textarea{width:100%;box-sizing:border-box;min-height:110px;padding:14px;border:1px solid #cbd5e1;border-radius:9px;font:16px Arial}
button{background:#1769aa;color:white;border:0;border-radius:8px;padding:12px 20px;font-size:15px;cursor:pointer;margin-top:12px}
#result{white-space:pre-wrap;line-height:1.55;margin-top:20px}.muted{color:#64748b;font-size:13px}
</style></head><body><header><h1>AI HR Portal</h1><div>Ask questions about company HR policies</div></header>
<main><section class="card"><h2>How can I help?</h2><p class="muted">Answers are generated from indexed policy documents. Verify important decisions with HR.</p>
<textarea id="q" placeholder="Example: What is the leave application process?"></textarea><br><button onclick="ask()">Ask HR Assistant</button>
<div id="result" aria-live="polite"></div></section></main>
<script>
async function ask(){const q=document.getElementById('q').value;const r=document.getElementById('result');r.textContent='Thinking…';
try{const res=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
const data=await res.json();if(!res.ok)throw new Error(data.detail||'Request failed');
r.textContent=data.answer+'\\n\\nSources: '+(data.sources||[]).join(', ');
}catch(e){r.textContent='Error: '+e.message}}
</script></body></html>""")

@app.post("/ask")
def ask(payload: AskRequest):
    try:
        return answer_question(payload.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        # Keep server details out of API responses; inspect application logs for diagnostics.
        raise HTTPException(status_code=500, detail="The assistant could not process the request. Check server configuration and logs.")
