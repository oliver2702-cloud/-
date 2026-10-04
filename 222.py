import streamlit as st
import json
import os
import random
import time
import socket
from datetime import datetime
import pandas as pd

# --- 1. 頁面與賽博龐克 CSS 注入 ---
st.set_page_config(
    page_title="情報天網 SKYNET Terminal v8.0 Pro",
    page_icon="🕸️️",
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
DB_FILE = "tasks_data.json"
CHAT_FILE = "chat_history.json"
PRIVATE_CHAT_FILE = "private_chats.json"
USERS_FILE = "users.json"
LOG_FILE = "logs.json"
SCAN_LOGS_FILE = "face_scan_logs.json"
CONFIG_FILE = "system_config.json"
MARKET_FILE = "market_rates.json"

for path in [IMAGE_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

class DataManager:
    @staticmethod
    def load(file):
        if not os.path.exists(file) or os.path.getsize(file) < 2:
            return {} if "config" in file or "market" in file or "private" in file else []
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {} if "config" in file or "market" in file or "private" in file else []
        
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
            st.error(f"寫入失敗: {str(e)}")

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

# 初始化使用者資料（預設特工個資庫）
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
def decrypt_morse(morse):
    res = []
    for code in morse.split(' '):
        res.append(REVERSE_MORSE.get(code, code))
    return ''.join(res)

# --- 3. 身分驗證系統 ---
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.update({"authenticated": False, "user": None})
    if st.session_state["authenticated"]:
        return True

    st.markdown("""
        <div style='background: radial-gradient(circle, #081024 0%, #010408 100%); padding: 25px; border-radius: 12px; border: 2px solid #39ff14; text-align: center; margin-bottom: 25px;'>
            <h1 style='color: #39ff14; text-shadow: 0 0 15px #39ff14;'>🌐 SKYNET TERMINAL v8.0</h1>
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

    # 系統頁籤選單
    tabs = st.tabs([
        "📷 視訊面部掃描", "📜 任務大廳", "➕ 發布任務", "🎯 戰情回報",
        "🏆 特工榜單", "📻 訊號傳譯器", "🗣️ 廣播頻道", "🔒 私密通訊", "⚙️ 指揮官管理專區"
    ])

    # --- TAB 0: 視訊面部掃描 ---
    with tabs[0]:
        st.subheader("📷 視訊面部身份掃描與自動回傳")
        st.caption("拍攝的面部快照與網路 IP 資料將即時傳送至管理員端備查。")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            cam_img = st.camera_input("開啟鏡頭執行特工面部掃描")
        
        with c2:
            st.markdown("##### 📌 當前掃描環境資料")
            current_ip = get_client_ip()
            st.write(f"・綁定 IP: `{current_ip}`")
            st.write(f"・操作特工: `{current_agent}`")
            st.write(f"・時間: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
            
            if cam_img is not None:
                st.image(cam_img, caption="快照預覽", width=220)
                if st.button("🚀 傳送截圖與資料給管理員", type="primary", use_container_width=True):
                    file_name = f"{current_agent}_{int(time.time())}.png"
                    file_path = os.path.join(IMAGE_DIR, file_name)
                    with open(file_path, "wb") as f:
                        f.write(cam_img.getvalue())
                    
                    scan_logs = DataManager.load(SCAN_LOGS_FILE)
                    scan_logs.insert(0, {
                        "agent": current_agent,
                        "ip": current_ip,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "image_path": file_path
                    })
                    DataManager.save(SCAN_LOGS_FILE, scan_logs)
                    log_activity("完成了視訊面部掃描並傳送紀錄給管理員", current_agent)
                    st.success("✅ 面部掃描截圖已成功安全傳送給管理員！")

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

    # --- TAB 6: 廣播頻道 ---
    with tabs[6]:
        chats = DataManager.load(CHAT_FILE)
        st.subheader("🗣️ 公共廣播大廳")
        for c in chats[-10:]:
            st.write(f"**[{c.get('sender')}]**: {c.get('text')}")
        with st.form("chat_form"):
            msg = st.text_input("輸入廣播訊息")
            if st.form_submit_button("發射訊息") and msg:
                chats.append({"sender": current_agent, "text": msg})
                DataManager.save(CHAT_FILE, chats)
                st.rerun()

    # --- TAB 7: 私密通訊 ---
    with tabs[7]:
        p_chats = DataManager.load(PRIVATE_CHAT_FILE)
        st.subheader("🔒 端到端加密對話")
        others = [u.get("user") for u in users if u.get("user") != current_agent]
        if others:
            target = st.selectbox("選擇通訊對象", others)
            pair = "_".join(sorted([current_agent, target]))
            history = p_chats.get(pair, [])
            for p in history[-8:]:
                st.write(f"**[{p['sender']}]**: {p['text']}")
            with st.form("p_chat_form"):
                p_msg = st.text_input("輸入加密對話")
                if st.form_submit_button("發送") and p_msg:
                    history.append({"sender": current_agent, "text": p_msg})
                    p_chats[pair] = history
                    DataManager.save(PRIVATE_CHAT_FILE, p_chats)
                    st.rerun()

    # --- TAB 8: 指揮官管理專區 (管理員專屬) ---
    with tabs[8]:
        st.subheader("⚙️ 指揮中心與特工機密檔案庫")
        if not is_admin:
            st.error("⛔ 存取拒絕！此分頁僅限管理員 (agent_alpha) 開啟。")
        else:
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["👤 特工完整個資庫", "📸 收到之面部掃描截圖", "🔑 特工審核與日誌"])
            
            # 1. 管理員專用特工個資面板
            with admin_tab1:
                st.markdown("#### 📋 系統機密特工個資總覽")
                for u in users:
                    prof = u.get("profile", {})
                    with st.expander(f"特工代號: {u.get('user')} ({prof.get('real_name', '未登記')})", expanded=False):
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            st.image(prof.get("avatar", "https://api.dicebear.com/7.x/bottts/svg?seed=default"), width=130)
                        with col_b:
                            st.markdown(f"**特工識別碼：** `{u.get('user')}`")
                            st.markdown(f"**真實姓名：** {prof.get('real_name', 'N/A')}")
                            st.markdown(f"**性別：** {prof.get('gender', 'N/A')}")
                            st.markdown(f"**綁定電腦 IP：** `{prof.get('ip_address', 'N/A')}`")
                            st.markdown(f"**通訊/居住地址：** {prof.get('address', 'N/A')}")
                            st.markdown(f"**當前階級：** `{u.get('rank')}` | **PTS:** `{u.get('points')}`")

            # 2. 接收到的面部掃描截圖
            with admin_tab2:
                st.markdown("#### 📥 特工回傳之面部掃描紀錄")
                scans = DataManager.load(SCAN_LOGS_FILE)
                if not scans:
                    st.info("尚未收到任何面部掃描回傳。")
                for s in scans:
                    with st.container(border=True):
                        col_s1, col_s2 = st.columns([1, 2])
                        with col_s1:
                            if os.path.exists(s.get("image_path", "")):
                                st.image(s.get("image_path"), width=200)
                        with col_s2:
                            st.markdown(f"**回傳特工：** `{s.get('agent')}`")
                            st.markdown(f"**來源 IP：** `{s.get('ip')}`")
                            st.markdown(f"**掃描時間：** {s.get('timestamp')}")

            # 3. 審核與日誌
            with admin_tab3:
                st.markdown("#### 📝 新特工審核")
                pending = [u for u in users if u.get("status") == "pending"]
                if not pending:
                    st.info("無待審核申請。")
                for pu in pending:
                    st.write(f"申請人: **{pu.get('user')}** (真實姓名: {pu.get('profile', {}).get('real_name')})")
                    if st.button("批准連線", key=f"app_{pu.get('user')}"):
                        pu["status"] = "active"
                        DataManager.save(USERS_FILE, users)
                        st.success("已核准！")
                        st.rerun()
                
                st.divider()
                st.markdown("#### 📜 系統日誌")
                st.json(DataManager.load(LOG_FILE))
