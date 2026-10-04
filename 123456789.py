import streamlit as st
import json
import os
import random
import time
import socket
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw

# --- 1. 頁面與賽博龐克 CSS 注入 ---
st.set_page_config(
    page_title="情報天網 SKYNET Terminal v9.0 Pro",
    page_icon="🕸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #03060f;
        color: #39ff14;
        font-family: 'Courier New', Courier, monospace;
    }
    section[data-testid="stSidebar"] {
        background-color: #010307 !important;
        border-right: 2px solid #39ff14 !important;
        box-shadow: 5px 0 20px rgba(57, 255, 20, 0.2) !important;
    }
    div[data-testid="stForm"] {
        border: 1px solid #39ff14 !important;
        background-color: #060c18 !important;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.2) !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #071504 0%, #010401 100%) !important;
        color: #39ff14 !important;
        border: 1px solid #39ff14 !important;
        box-shadow: 0 0 10px rgba(57, 255, 20, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px #39ff14;
        border-radius: 8px !important;
    }
    .stButton button:hover {
        background: #39ff14 !important;
        color: #010307 !important;
        box-shadow: 0 0 30px #39ff14 !important;
    }
    input, textarea, select {
        background-color: #040812 !important;
        color: #39ff14 !important;
        border: 1px solid #00ffcc !important;
        box-shadow: inset 0 0 8px rgba(0, 255, 204, 0.2) !important;
    }
    button[data-baseweb="tab"] {
        color: #00ffcc !important;
        font-size: 15px !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #39ff14 !important;
        border-bottom-color: #39ff14 !important;
        text-shadow: 0 0 15px #39ff14;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 檔案路徑與資料庫初始化 ---
IMAGE_DIR = "face_scans"
CHAT_FILE_DIR = "chat_files"
DB_FILE = "tasks_data.json"
CHAT_FILE = "chat_history.json"
PRIVATE_CHAT_FILE = "private_chats.json"
USERS_FILE = "users.json"
LOG_FILE = "logs.json"
SCAN_LOGS_FILE = "face_scan_logs.json"

for path in [IMAGE_DIR, CHAT_FILE_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

class DataManager:
    @staticmethod
    def load(file):
        if not os.path.exists(file) or os.path.getsize(file) < 2:
            return {} if "private" in file else []
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {} if "private" in file else []
        
    @staticmethod
    def save(file, data):
        try:
            tmp_file = f"{file}.tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            if os.path.exists(tmp_file):
                if os.path.exists(file):
                    os.remove(file)
                os.rename(tmp_file, file)
        except Exception as e:
            st.error(f"資料寫入失敗: {str(e)}")

def log_activity(event, agent="系統"):
    logs = DataManager.load(LOG_FILE)
    logs.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "agent": agent, "event": event})
    DataManager.save(LOG_FILE, logs[:100])

def get_client_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# 預設特工資料庫
DEFAULT_USERS = [
    {
        "user": "agent_007", "pwd": "pwd7788", "status": "active", "rank": "王牌特工", "points": 1500, "failed_count": 0,
        "profile": {"real_name": "詹姆斯", "gender": "男", "ip_address": "192.168.1.107", "address": "臺北市信義區信義路五段 7 號", "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=agent_007"}
    },
    {
        "user": "agent_008", "pwd": "pwd8899", "status": "active", "rank": "資深探員", "points": 800, "failed_count": 1,
        "profile": {"real_name": "林小雅", "gender": "女", "ip_address": "10.0.0.42", "address": "新北市板橋區縣民大道二段 7 號", "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=agent_008"}
    }
]

DEFAULT_ADMIN = {"agent_alpha": "alpha7788"}

if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) < 5:
    DataManager.save(USERS_FILE, DEFAULT_USERS)

# 摩斯密碼字典
MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'}
REVERSE_MORSE = {v: k for k, v in MORSE_CODE_DICT.items()}

def encrypt_morse(msg): return ' '.join([MORSE_CODE_DICT.get(c, c) for c in msg.upper()])
def decrypt_morse(morse): return ''.join([REVERSE_MORSE.get(code, code) for code in morse.split(' ')])

# --- 3. 身分驗證機制 ---
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.update({"authenticated": False, "user": None})
    if st.session_state["authenticated"]:
        return True

    st.markdown("""
        <div style='background: radial-gradient(circle, #081024 0%, #010408 100%); padding: 25px; border-radius: 12px; border: 2px solid #39ff14; text-align: center; margin-bottom: 25px;'>
            <h1 style='color: #39ff14; text-shadow: 0 0 15px #39ff14;'>🌐 SKYNET TERMINAL v9.0 Pro</h1>
            <p style='color: #00ffcc; font-weight: bold;'>[中央安全防火陣列 - 特工安全驗證通道]</p>
        </div>
    """, unsafe_allow_html=True)

    mode = st.radio("驗證模式", ["登入系統", "申請探員註冊"], horizontal=True, label_visibility="collapsed")
    
    if mode == "登入系統":
        u = st.text_input("👤 探員識別碼 (ID)", key="login_uid")
        p = st.text_input("🔑 安全授權碼 (ACCESS PASS)", type="password", key="login_pwd")
        if st.button("🔐 執行身分安全認證", use_container_width=True):
            if u in DEFAULT_ADMIN and DEFAULT_ADMIN[u] == p:
                st.session_state.update({"authenticated": True, "user": u})
                st.rerun()
            users = DataManager.load(USERS_FILE)
            user = next((x for x in users if x.get("user") == u and x.get("pwd") == p), None)
            if user and user.get("status") == "active":
                st.session_state.update({"authenticated": True, "user": u})
                log_activity("登入系統", u)
                st.rerun()
            else:
                st.error("認證失敗或該特工帳號尚未獲批啟用。")
    else:
        new_u = st.text_input("👤 創立新識別碼", key="reg_uid")
        new_p = st.text_input("🔑 設定授權碼", type="password", key="reg_pwd")
        real_name = st.text_input("真實姓名")
        gender = st.selectbox("性別", ["男", "女", "保密"])
        address = st.text_input("通訊地址")
        
        if st.button("📝 提交特工註冊", use_container_width=True):
            if not new_u or not new_p or not real_name:
                st.error("請完整填寫註冊資料！")
            else:
                users = DataManager.load(USERS_FILE)
                if any(x.get("user") == new_u for x in users) or new_u in DEFAULT_ADMIN:
                    st.error("該識別碼已被註冊。")
                else:
                    users.append({
                        "user": new_u, "pwd": new_p, "status": "pending", "rank": "菜鳥特工", "points": 100, "failed_count": 0,
                        "profile": {
                            "real_name": real_name, "gender": gender, "ip_address": get_client_ip(), "address": address,
                            "avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={new_u}"
                        }
                    })
                    DataManager.save(USERS_FILE, users)
                    st.success("✅ 註冊已提交，請等待管理員審核。")
    return False

# --- 4. 核心主程式 ---
if authenticate():
    current_agent = st.session_state["user"]
    is_admin = (current_agent == "agent_alpha")
    
    users = DataManager.load(USERS_FILE)
    u_data = next((u for u in users if u.get("user") == current_agent), None)
    pts = u_data.get("points", 0) if u_data else (999999 if is_admin else 0)
    rank = u_data.get("rank", "菜鳥特工") if u_data else ("最高指揮官" if is_admin else "快捷探員")

    st.sidebar.markdown(f"""
        <div style='background-color:#020612; padding:15px; border-radius:10px; border:1px solid #39ff14; text-align:center;'>
            <span style='color:#39ff14; font-size:1.1em; font-weight:bold;'>📡 特工戰情端</span><br>
            <span style='color:#39ff14;'>● ONLINE</span>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.info(f"**👤 識別碼:** `{current_agent}`\n\n**🎖️ 階級:** `{rank}`\n\n**💎 點數:** `{pts}` PTS")
    
    if st.sidebar.button("🔒 安全登出", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    # 主分頁頁籤
    tabs = st.tabs([
        "📷 視訊面部掃描", "📜 任務大廳", "➕ 發布任務", "🎯 戰情回報",
        "🏆 特工榜單", "📻 訊號傳譯器", "🗣️ 廣播頻道", "🔒 私密通訊", "⚙️ 指揮官管理專區"
    ])

    # --- TAB 0: 視訊面部掃描（增加模擬 AI 人臉檢測邊框） ---
    with tabs[0]:
        st.subheader("📷 視訊面部身份掃描與 AI 識別傳送")
        st.caption("拍攝快照將自動進行特徵框選並實時傳送至管理員端。")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            cam_img = st.camera_input("開啟鏡頭執行特工面部掃描")
        
        with c2:
            st.markdown("##### 📌 當前掃描與檢測設定")
            threshold = st.slider("AI 信心度門檻", 50, 99, 85)
            current_ip = get_client_ip()
            st.write(f"・綁定 IP: `{current_ip}`")
            st.write(f"・操作特工: `{current_agent}`")
            st.write(f"・時間: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
            
            if cam_img is not None:
                img = Image.open(cam_img)
                draw = ImageDraw.Draw(img)
                w, h = img.size
                # 模擬 AI 特徵點框選
                draw.rectangle([w*0.3, h*0.2, w*0.7, h*0.8], outline="#39ff14", width=4)
                draw.text((w*0.3, h*0.15), f"FACE DETECTED: {threshold}%", fill="#39ff14")
                
                st.image(img, caption="AI 特徵標註快照", width=240)
                if st.button("🚀 傳送標註截圖與資料給管理員", type="primary", use_container_width=True):
                    file_name = f"{current_agent}_{int(time.time())}.png"
                    file_path = os.path.join(IMAGE_DIR, file_name)
                    img.save(file_path)
                    
                    scan_logs = DataManager.load(SCAN_LOGS_FILE)
                    scan_logs.insert(0, {
                        "id": str(int(time.time())),
                        "agent": current_agent,
                        "ip": current_ip,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "image_path": file_path
                    })
                    DataManager.save(SCAN_LOGS_FILE, scan_logs)
                    log_activity("完成了視訊面部掃描與 AI 特徵傳送", current_agent)
                    st.success("✅ 面部掃描截圖已成功傳送給管理員！")

    # --- TAB 1: 任務大廳 ---
    with tabs[1]:
        tasks = DataManager.load(DB_FILE)
        st.subheader("📜 探員戰術懸賞告示")
        available = [t for t in tasks if t.get("status") == "待接取" and t.get("posted_by") != current_agent]
        if not available:
            st.info("當前無懸賞任務。")
        for t in available:
            with st.container(border=True):
                st.write(f"🎯 **{t.get('task_name')}** | 💎 **賞金:** {t.get('reward')} PTS | **發起人:** {t.get('posted_by')}")
                if st.button("📥 接取任務", key=f"ac_{t.get('id')}"):
                    t.update({"status": "已接取", "accepted_by": current_agent})
                    DataManager.save(DB_FILE, tasks)
                    st.success("接取成功！")
                    st.rerun()

    # --- TAB 2: 發布任務 ---
    with tabs[2]:
        tasks = DataManager.load(DB_FILE)
        st.subheader("➕ 發布全新戰術懸賞令")
        with st.form("post_task"):
            n = st.text_input("任務目標")
            r = st.number_input("託管賞金 (PTS)", min_value=10, value=100)
            if st.form_submit_button("🚀 發布廣播"):
                if not is_admin and pts < r:
                    st.error("餘額不足！")
                else:
                    if u_data and not is_admin:
                        u_data["points"] -= r
                        DataManager.save(USERS_FILE, users)
                    tasks.append({"id": str(int(time.time())), "task_name": n, "reward": r, "status": "待接取", "posted_by": current_agent})
                    DataManager.save(DB_FILE, tasks)
                    st.success("懸賞發布成功！")
                    st.rerun()

    # --- TAB 3: 戰情回報 ---
    with tabs[3]:
        tasks = DataManager.load(DB_FILE)
        st.subheader("🎯 指令進度與審核")
        my_tasks = [t for t in tasks if t.get("accepted_by") == current_agent and t.get("status") == "已接取"]
        for t in my_tasks:
            with st.container(border=True):
                st.write(f"**目標:** {t.get('task_name')}")
                if st.button("📤 提交成果回報", key=f"rep_{t.get('id')}"):
                    t["status"] = "等待審核"
                    DataManager.save(DB_FILE, tasks)
                    st.success("成果已上報。")
                    st.rerun()

    # --- TAB 4: 特工榜單 ---
    with tabs[4]:
        st.subheader("🏆 全網特工榮譽排行榜")
        sorted_u = sorted([u for u in users if u.get("status") == "active"], key=lambda x: x.get("points", 0), reverse=True)
        st.dataframe(pd.DataFrame([
            {"特工識別": u.get("user"), "階級": u.get("rank"), "PTS 積分": u.get("points")}
            for u in sorted_u
        ]), use_container_width=True)

    # --- TAB 5: 訊號傳譯器 ---
    with tabs[5]:
        st.subheader("📻 摩斯密碼轉譯器")
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            raw = st.text_area("輸入文字 (英文/數字)")
            if st.button("加密為摩斯電碼"): st.code(encrypt_morse(raw))
        with c_m2:
            code = st.text_area("輸入摩斯電碼")
            if st.button("解密電碼"): st.success(decrypt_morse(code))

    # --- TAB 6: 廣播頻道（增加清理與刪除功能） ---
    with tabs[6]:
        chats = DataManager.load(CHAT_FILE)
        st.subheader("🗣️ 公共廣播大廳")
        
        if is_admin and chats:
            if st.button("🗑️ [管理員] 清空所有廣播紀錄", type="secondary"):
                DataManager.save(CHAT_FILE, [])
                st.success("公共廣播紀錄已全部清空。")
                st.rerun()

        for idx, c in enumerate(chats[-12:]):
            cols = st.columns([4, 1])
            with cols[0]:
                st.write(f"**[{c.get('sender')}]**: {c.get('text')}")
            with cols[1]:
                if is_admin or c.get('sender') == current_agent:
                    if st.button("刪除", key=f"del_chat_{idx}"):
                        chats.remove(c)
                        DataManager.save(CHAT_FILE, chats)
                        st.rerun()
                        
        with st.form("chat_form"):
            msg = st.text_input("輸入廣播訊息")
            if st.form_submit_button("發射訊息") and msg:
                chats.append({"sender": current_agent, "text": msg})
                DataManager.save(CHAT_FILE, chats)
                st.rerun()

    # --- TAB 7: 私密通訊（支援檔案上傳與訊息刪除） ---
    with tabs[7]:
        p_chats = DataManager.load(PRIVATE_CHAT_FILE)
        st.subheader("🔒 端到端加密對話頻道")
        others = [u.get("user") for u in users if u.get("user") != current_agent]
        if others:
            col_target, col_del = st.columns([3, 1])
            with col_target:
                target = st.selectbox("選擇通訊對象", others)
            pair = "_".join(sorted([current_agent, target]))
            history = p_chats.get(pair, [])

            with col_del:
                st.write("")
                st.write("")
                if st.button("🗑️ 清空此私訊頻道", key=f"del_p_chan_{pair}"):
                    p_chats[pair] = []
                    DataManager.save(PRIVATE_CHAT_FILE, p_chats)
                    st.success("私密頻道已重置。")
                    st.rerun()

            for idx, p in enumerate(history[-10:]):
                st.write(f"**[{p['sender']}]**: {p['text']}")
                if p.get("file"):
                    st.image(p["file"], width=180)

            with st.form("p_chat_form"):
                p_msg = st.text_input("輸入加密對話")
                up_file = st.file_uploader("📎 附加機密檔案/圖片", type=["png", "jpg", "jpeg"])
                if st.form_submit_button("安全傳送") and (p_msg or up_file):
                    file_path = None
                    if up_file:
                        file_path = os.path.join(CHAT_FILE_DIR, f"{int(time.time())}_{up_file.name}")
                        with open(file_path, "wb") as f:
                            f.write(up_file.getvalue())
                    history.append({"sender": current_agent, "text": p_msg, "file": file_path})
                    p_chats[pair] = history
                    DataManager.save(PRIVATE_CHAT_FILE, p_chats)
                    st.rerun()

    # --- TAB 8: 指揮官管理專區 (完整管理與刪除權限) ---
    with tabs[8]:
        st.subheader("⚙️ 指揮中心與特工機密檔案庫")
        if not is_admin:
            st.error("⛔ 存取拒絕！此分頁僅限最高管理員 (agent_alpha) 開啟。")
        else:
            admin_tab1, admin_tab2, admin_tab3 = st.tabs([
                "👤 特工個資與編輯/刪除", "📸 接收掃描截圖管理", "🔑 審核與日誌"
            ])
            
            # 1. 管理員專用：個資檢視、動態修改與刪除
            with admin_tab1:
                st.markdown("#### 📋 系統機密特工個資總覽")
                
                # 一鍵匯出特工個資功能
                if st.download_button("📥 匯出全廠特工機密 JSON 檔案", data=json.dumps(users, ensure_ascii=False, indent=4), file_name="agent_profiles_backup.json", mime="application/json"):
                    st.toast("匯出備份成功！")

                st.divider()

                for u in users:
                    prof = u.get("profile", {})
                    u_id = u.get('user')
                    with st.expander(f"特工代號: {u_id} ({prof.get('real_name', '未登記')})", expanded=False):
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            st.image(prof.get("avatar", "https://api.dicebear.com/7.x/bottts/svg?seed=default"), width=130)
                            
                            # 特工刪除按鈕
                            if st.button(f"❌ 徹底開除/刪除特工 [{u_id}]", key=f"del_usr_{u_id}", type="primary"):
                                users = [x for x in users if x.get("user") != u_id]
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"刪除了特工 [{u_id}] 的所有個資與帳號", current_agent)
                                st.success(f"已將特工 {u_id} 從資料庫除名。")
                                st.rerun()

                        with col_b:
                            with st.form(key=f"edit_form_{u_id}"):
                                st.markdown(f"**特工識別碼：** `{u_id}`")
                                edit_name = st.text_input("真實姓名", value=prof.get("real_name", ""))
                                edit_gender = st.selectbox("性別", ["男", "女", "保密"], index=["男", "女", "保密"].index(prof.get("gender", "男")) if prof.get("gender") in ["男", "女", "保密"] else 0)
                                edit_ip = st.text_input("綁定電腦 IP", value=prof.get("ip_address", ""))
                                edit_addr = st.text_input("通訊地址", value=prof.get("address", ""))
                                edit_pts = st.number_input("PTS 點數調整", value=int(u.get("points", 0)))
                                
                                if st.form_submit_button("💾 儲存個資變更"):
                                    u["points"] = edit_pts
                                    u["profile"] = {
                                        "real_name": edit_name,
                                        "gender": edit_gender,
                                        "ip_address": edit_ip,
                                        "address": edit_addr,
                                        "avatar": prof.get("avatar")
                                    }
                                    DataManager.save(USERS_FILE, users)
                                    st.success("個資升級成功！")
                                    st.rerun()

            # 2. 面部掃描紀錄刪除與審閱
            with admin_tab2:
                st.markdown("#### 📥 特工回傳之面部掃描紀錄")
                scans = DataManager.load(SCAN_LOGS_FILE)
                
                if scans and st.button("🗑️ 清空所有掃描圖片與紀錄"):
                    for s in scans:
                        if os.path.exists(s.get("image_path", "")):
                            try: os.remove(s.get("image_path"))
                            except: pass
                    DataManager.save(SCAN_LOGS_FILE, [])
                    st.success("清空完畢。")
                    st.rerun()

                if not scans:
                    st.info("目前尚無面部掃描紀錄。")
                for s in scans:
                    with st.container(border=True):
                        col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
                        with col_s1:
                            if os.path.exists(s.get("image_path", "")):
                                st.image(s.get("image_path"), width=180)
                        with col_s2:
                            st.markdown(f"**回傳特工：** `{s.get('agent')}`")
                            st.markdown(f"**來源 IP：** `{s.get('ip')}`")
                            st.markdown(f"**掃描時間：** {s.get('timestamp')}")
                        with col_s3:
                            if st.button("刪除此紀錄", key=f"del_scan_{s.get('id', s.get('timestamp'))}"):
                                if os.path.exists(s.get("image_path", "")):
                                    try: os.remove(s.get("image_path"))
                                    except: pass
                                scans.remove(s)
                                DataManager.save(SCAN_LOGS_FILE, scans)
                                st.rerun()

            # 3. 審核與系統日誌
            with admin_tab3:
                st.markdown("#### 📝 新特工審核")
                pending = [u for u in users if u.get("status") == "pending"]
                if not pending:
                    st.info("無待審核申請。")
                for pu in pending:
                    p_id = pu.get("user")
                    st.write(f"申請人: **{p_id}** (姓名: {pu.get('profile', {}).get('real_name')})")
                    c_p1, c_p2 = st.columns(2)
                    with c_p1:
                        if st.button("✅ 批准連線", key=f"app_{p_id}"):
                            pu["status"] = "active"
                            DataManager.save(USERS_FILE, users)
                            st.success("已核准！")
                            st.rerun()
                    with c_p2:
                        if st.button("❌ 駁回並刪除", key=f"rej_{p_id}"):
                            users.remove(pu)
                            DataManager.save(USERS_FILE, users)
                            st.warning("已駁回申請。")
                            st.rerun()
                
                st.divider()
                st.markdown("#### 📜 系統操作日誌 (Log)")
                if st.button("🗑️ 清空系統日誌"):
                    DataManager.save(LOG_FILE, [])
                    st.rerun()
                st.json(DataManager.load(LOG_FILE))
