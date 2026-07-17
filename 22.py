import os
import io
from typing import Generator
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

# 深度檔案解析套件
import pypdf
import docx
import openpyxl
import pptx
import pandas as pd

# LangChain 與 向量庫套件
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. 核心配置 (Chroma 永久保存版)
# ==========================================
app = FastAPI(title="Enterprise Lean RAG Hub")

CHROMA_PATH = "./chroma_db"
os.makedirs(CHROMA_PATH, exist_ok=True)

embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="bge-m3")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
vector_store = Chroma(
    client=chroma_client,
    collection_name="enterprise_lean_collection",
    embedding_function=embeddings
)

# ==========================================
# 2. 全格式文件解析與覆蓋更新
# ==========================================
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename
        file_ext = os.path.splitext(filename)[1].lower()
        text_content = ""

        if file_ext == ".txt":
            text_content = contents.decode("utf-8", errors="ignore")
        elif file_ext == ".pdf":
            pdf_reader = pypdf.PdfReader(io.BytesIO(contents))
            text_content = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        elif file_ext == ".docx":
            doc = docx.Document(io.BytesIO(contents))
            text_content = "\n".join([p.text for p in doc.paragraphs])
        elif file_ext == ".xlsx":
            wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
            text_content = "\n".join([", ".join([str(c) for c in r if c is not None]) for s in wb.worksheets for r in s.iter_rows(values_only=True)])
        elif file_ext == ".pptx":
            prs = pptx.Presentation(io.BytesIO(contents))
            text_content = "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
        elif file_ext == ".csv":
            df = pd.read_csv(io.BytesIO(contents))
            text_content = df.to_string(index=False)
        else:
            return {"status": "error", "detail": f"不支援 {file_ext} 格式"}

        if not text_content.strip():
            return {"status": "error", "detail": "檔案內查無有效文字"}

        try:
            vector_store.delete(where={"source": filename})
        except Exception:
            pass

        chunks = text_splitter.split_text(text_content)
        docs = [LCDocument(page_content=ch, metadata={"source": filename}) for ch in chunks]
        vector_store.add_documents(docs)

        return {"status": "success", "filename": filename, "chunks_added": len(chunks)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# ==========================================
# 3. RAG 檢索生成與多引用
# ==========================================
def generate_rag_stream(question: str) -> Generator[str, None, None]:
    if len(question.strip()) < 2:
        yield "data: ⚠️ 提問字數太短，請輸入更具體的完整問題。\\n\\n"
        return

    try:
        raw_docs = vector_store.similarity_search_with_score(question, k=8)
    except Exception:
        raw_docs = []

    if not raw_docs:
        yield "data: 📢 知識庫目前尚無資料，請先上傳文件建立索引。\\n\\n"
        return

    seen_content = set()
    valid_docs = []
    for doc, score in raw_docs:
        if score < 1.4 and doc.page_content not in seen_content:
            seen_content.add(doc.page_content)
            valid_docs.append(doc)
    valid_docs = valid_docs[:4]

    if not valid_docs:
        yield "data: 🔍 搜尋了硬碟資料庫，但查無信心度足夠的相符片段。\\n\\n"
        return

    context = "\n".join([f"【來源: {d.metadata.get('source')}】: {d.page_content}" for d in valid_docs])
    system_prompt = (
        "你是一位嚴謹的企業知識庫助手。請完全且僅能依據下方的【參考資料】回答問題。\n"
        "如果參考資料不足以完整回答，請直接回答『知識庫沒有相關資料』，絕對不能自行編造或延伸記憶。\n\n"
        f"【參考資料】:\n{context}\n\n"
        f"【使用者問題】: {question}"
    )

    llm = ChatOllama(base_url="http://localhost:11434", model="qwen2.5:7b", temperature=0.0, streaming=True)
    for chunk in llm.stream(system_prompt):
        yield f"data: {chunk.content.replace(chr(10), '\\n')}\n\n"
    
    sources = list({d.metadata["source"] for d in valid_docs})
    yield "data: \\n\\n---\\n### 📌 交叉引用與來源明細：\\n"
    for s in sources:
        yield f"data: * `{s}`\\n"
    yield "data: \\n\\n"

@app.get("/query")
def chat_endpoint(question: str):
    return StreamingResponse(generate_rag_stream(question), media_type="text/event-stream")

# ==========================================
# 4. 統計數據路由
# ==========================================
@app.get("/stats")
def stats():
    try:
        count = vector_store._collection.count()
        metadatas = vector_store._collection.get(include=['metadatas'])['metadatas']
        doc_count = len(set([m['source'] for m in metadatas if m and 'source' in m]))
    except Exception:
        count, doc_count = 0, 0
    return {"chunks": count, "documents": doc_count}

# ==========================================
# 5. 精美 UI 網頁 (原生 HTML5/JS，100% 不崩潰，完美支援平板)
# ==========================================
@app.get("/", response_class=HTMLResponse)
def index_page():
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>在地智能知識庫 (持久化版)</title>
        <style>
            :root { --bg: #f4f6f9; --box-bg: white; --text: #333; --border: #ccc; }
            @media (prefers-color-scheme: dark) {
                :root { --bg: #121212; --box-bg: #1e1e1e; --text: #e0e0e0; --border: #444; }
            }
            body { font-family: system-ui, sans-serif; margin: 20px; background: var(--bg); color: var(--text); transition: 0.3s; }
            .box { background: var(--box-bg); padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border); }
            .input-group { display: flex; gap: 10px; width: 100%; }
            input[type="text"] { flex: 1; padding: 14px; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 6px; font-size: 16px; -webkit-appearance: none; }
            button { padding: 14px 28px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 6px; font-weight: bold; font-size: 16px; transition: 0.2s; }
            button:hover { background: #0056b3; }
            #chat { background: var(--bg); border: 1px solid var(--border); padding: 15px; height: 380px; overflow-y: auto; white-space: pre-line; margin-bottom: 12px; border-radius: 6px; font-size: 15px; }
            .drop-zone { border: 2px dashed #007bff; padding: 35px 20px; text-align: center; border-radius: 8px; cursor: pointer; margin-bottom: 10px; background: rgba(0,123,255,0.04); transition: 0.2s; min-height: 110px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
            .drop-zone.hover { background: rgba(0,123,255,0.15); border-color: #0056b3; }
            .stats-text { font-size: 13px; opacity: 0.8; margin-top: 5px; font-weight: 500; }
            h1 { font-size: 1.65rem; margin-bottom: 15px; text-align: center; }
            h2 { font-size: 1.15rem; margin-top: 0; }
            @media (min-width: 768px) {
                body { margin: 40px auto; max-width: 900px; }
                h1 { text-align: left; }
            }
        </style>
    </head>
    <body>
        <h1>🏢 本地企業智能知識庫系統</h1>
        <div class="box">
            <h2>1. 文件核心匯入中心</h2>
            <div id="dropZone" class="drop-zone">
                <strong style="color: #007bff;">點擊此處選取檔案</strong> 或將檔案拖曳至此<br>
                <span style="font-size:12px; opacity:0.7; margin-top: 5px;">(支援 PDF, DOCX, XLSX, PPTX, CSV, TXT)</span>
            </div>
            <input type="file" id="fileInput" style="display:none;">
            <p id="uploadStatus" style="color: #007bff; font-size: 14px; font-weight:bold; margin: 5px 0;"></p>
            <div class="stats-text" id="statsDisplay">讀取數據庫統計中...</div>
        </div>
        <div class="box">
            <h2>2. 企業規章文檔檢索</h2>
            <div id="chat">等待上傳文檔或直接對現存硬碟知識庫提問...</div>
            <div class="input-group">
                <input type="text" id="questionInput" placeholder="請輸入您的問題..." onkeypress="if(event.keyCode==13) sendQuery()">
                <button onclick="sendQuery()">提問</button>
            </div>
        </div>
        <script>
            async function updateStats() {
                try {
                    const res = await fetch('/stats');
                    const d = await res.json();
                    document.getElementById('statsDisplay').innerText = `📊 目前本地儲存庫共包含： ${d.chunks} 個知識片段 (Chunks) / 存有 ${d.documents} 份獨立文檔`;
                } catch(e) {}
            }
            window.onload = updateStats;

            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            dropZone.onclick = () => fileInput.click();
            dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('hover'); };
            dropZone.ondragleave = () => dropZone.classList.remove('hover');
            dropZone.ondrop = (e) => {
                e.preventDefault();
                dropZone.classList.remove('hover');
                if (e.dataTransfer.files.length) {
                    fileInput.files = e.dataTransfer.files;
                    executeUpload();
                }
            };
            fileInput.onchange = () => { if(fileInput.files.length) executeUpload(); };

            async function executeUpload() {
                const status = document.getElementById('uploadStatus');
                const fd = new FormData();
                fd.append('file', fileInput.files[0]);
                status.style.color = '#007bff';
                status.innerText = `⏳ 正在為 "${fileInput.files[0].name}" 進行深度矩陣向量建檔，請稍候...`;
                try {
                    const res = await fetch('/upload', { method: 'POST', body: fd });
                    const r = await res.json();
                    if(r.status === 'success') {
                        status.style.color = '#28a745';
                        status.innerText = `✅ 成功覆蓋/更新！已轉換 ${r.chunks_added} 個語義區塊並安全儲存至硬碟。`;
                        updateStats();
                    } else {
                        status.style.color = '#dc3545';
                        status.innerText = '❌ 錯誤: ' + r.detail;
                    }
                } catch(err) {
                    status.style.color = '#dc3545';
                    status.innerText = '❌ 連線失敗，請檢查後端是否正常運行。';
                }
            }

            function sendQuery() {
                const qi = document.getElementById('questionInput');
                const cb = document.getElementById('chat');
                const q = qi.value.trim();
                if(!q) return;

                if(cb.innerText.includes('等待上傳文檔')) cb.innerHTML = '';
                cb.innerHTML += `<b>🙋 使用者:</b> ${q}\\n`;
                
                const aiBox = document.createElement('span');
                aiBox.innerHTML = '<b>🤖 助手:</b> 思考中...';
                cb.appendChild(aiBox);
                qi.value = '';
                cb.scrollTop = cb.scrollHeight;

                const es = new EventSource(`/query?question=${encodeURIComponent(q)}`);
                es.onmessage = function(e) {
                    if(aiBox.innerHTML.includes('思考中...')) { aiBox.innerHTML = '<b>🤖 助手:</b> '; }
                    aiBox.innerText += e.data.replace(/\\\\n/g, '\\n');
                    cb.scrollTop = cb.scrollHeight;
                };
                es.onerror = function() { es.close(); cb.innerHTML += '\\n'; };
            }
        </script>
    </body>
    </html>
    """

# ==========================================
# 6. 本地直接執行入口 (若用 Python main.py 啟動)
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
