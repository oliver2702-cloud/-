import streamlit as st
import json
import os
import random
import time
import base64
from datetime import datetime, timedelta
import pandas as pd

# --- 1. 核心安全配置與高級賽博龐克 CSS 注入 ---
st.set_page_config(
    page_title="情報天網 SKYNET Terminal v7.0 Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 極限優化外觀：注入高科技賽博龐克暗黑風格 CSS (含呼吸發光、霓虹流光、動態漸層特效)
st.markdown("""
<style>
    /* 全局背景與霓虹冷光字體 */
    .stApp {
        background-color: #03060f;
        color: #39ff14;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 調整 sidebar 風格 */
    section[data-testid="stSidebar"] {
        background-color: #010307 !important;
        border-right: 2px solid #39ff14 !important;
        box-shadow: 5px 0 20px rgba(57, 255, 20, 0.2) !important;
    }
    
    /* 自訂卡片流光發光外框 */
    div[data-testid="stForm"], div.element-container div.stAlert, .stButton button {
        border-radius: 8px !important;
    }
    
    div[data-testid="stForm"] {
        border: 1px solid #39ff14 !important;
        background-color: #060c18 !important;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.2) !important;
    }
    
    /* 特工風格霓虹按鈕 (綠色呼吸發光) */
    .stButton button {
        background: linear-gradient(135deg, #071504 0%, #010401 100%) !important;
        color: #39ff14 !important;
        border: 1px solid #39ff14 !important;
        box-shadow: 0 0 10px rgba(57, 255, 20, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px #39ff14;
    }
    
    .stButton button:hover {
        background: #39ff14 !important;
        color: #010307 !important;
        box-shadow: 0 0 30px #39ff14 !important;
        transform: translateY(-2px);
    }
    
    /* 橘色發光警示卡片與按鈕 */
    div.stButton button[p-type="primary"] {
        border-color: #ffaa00 !important;
        color: #ffaa00 !important;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.3) !important;
        text-shadow: 0 0 5px #ffaa00;
    }
    div.stButton button[p-type="primary"]:hover {
        background: #ffaa00 !important;
        color: #010307 !important;
        box-shadow: 0 0 30px #ffaa00 !important;
    }
    
    /* 輸入框科技感發光 */
    input, textarea, select {
        background-color: #040812 !important;
        color: #39ff14 !important;
        border: 1px solid #00ffcc !important;
        box-shadow: inset 0 0 8px rgba(0, 255, 204, 0.2) !important;
    }
    
    input:focus, textarea:focus {
        border-color: #39ff14 !important;
        box-shadow: 0 0 15px #39ff14 !important;
    }
    
    /* 頁籤美化 */
    button[data-baseweb="tab"] {
        color: #00ffcc !important;
        font-size: 16px !important;
        font-weight: bold !important;
        background-color: transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #39ff14 !important;
        border-bottom-color: #39ff14 !important;
        text-shadow: 0 0 15px #39ff14;
    }
    
    /* 數據閃爍動畫 */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    .neon-blink {
        animation: blink 1.8s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 模擬音波合成器 (生成 base64 音頻供 HTML5 播放) ---
def play_synth_sound(sound_type="beep"):
    """
    動態生成一段簡單的電子合成音波，利用 Streamlit 的 HTML 元件播放
    """
    if sound_type == "beep":
        audio_b64 = "UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQgAAAAAAAAA"
    elif sound_type == "static":
        audio_b64 = "UklGRjQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YRAA//8AAP//AAD//wAA//8="
    else:
        return
    st.markdown(f'<audio autoplay src="data:audio/wav;base64,{audio_b64}"></audio>', unsafe_allow_html=True)


# --- 3. 系統檔案路徑與自動初始化 ---
IMAGE_DIR = "task_images"
DB_FILE = "tasks_data.json"
CHAT_FILE = "chat_history.json"
PRIVATE_CHAT_FILE = "private_chats.json"
USERS_FILE = "users.json"
LOG_FILE = "logs.json"
SHOP_FILE = "shop_items.json"
CONFIG_FILE = "system_config.json"
INVEST_FILE = "invest_data.json"
MARKET_FILE = "market_rates.json"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 摩斯密碼字典 ---
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.', ' ': '/'
}
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

def encrypt_morse(message):
    cipher = []
    for letter in message.upper():
        if letter in MORSE_CODE_DICT:
            cipher.append(MORSE_CODE_DICT[letter])
        else:
            cipher.append(letter)
    return ' '.join(cipher)

def decrypt_morse(morse):
    morse += ' '
    decipher = ''
    citext = ''
    for letter in morse:
        if letter != ' ':
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                if citext in REVERSE_MORSE_DICT:
                    decipher += REVERSE_MORSE_DICT[citext]
                else:
                    decipher += citext
                citext = ''
    return decipher


# --- 4. 資料安全管理器 (原子寫入防鎖) ---
class DataManager:
    @staticmethod
    def load(file):
        if not os.path.exists(file) or os.path.getsize(file) < 2:
            return {} if "config" in file or "market" in file else []
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            if os.path.exists(file):
                os.rename(file, f"{file}.bak_{int(datetime.now().timestamp())}")
            return {} if "config" in file or "market" in file else []
        
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
            st.error(f"核心數據寫入失敗: {str(e)}")

def log_activity(event, agent="系統"):
    logs = DataManager.load(LOG_FILE)
    logs.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "agent": agent, "event": event})
    DataManager.save(LOG_FILE, logs[:100])

@st.cache_data(ttl=600)
def get_default_shop_items():
    return [
        {"id": "item_01", "name": "🔑 進階解密金鑰", "price": 500, "desc": "【滲透演練專用】破解高強度防禦，成功率額外 +30%。", "type": "normal"},
        {"id": "item_02", "name": "🛰️ 衛星追蹤權限", "price": 1200, "desc": "【滲透演練專用】捕捉防禦漏洞，獲得雙倍 (x2) PTS 獎勵。", "type": "normal"},
        {"id": "item_03", "name": "🧥 匿蹤防護斗篷", "price": 2000, "desc": "【滲透演練專用】免除失敗被追蹤扣除壽命的懲罰。", "type": "normal"},
        {"id": "item_04", "name": "🧪 奈米修復血清", "price": 1500, "desc": "【背包主動使用】可於背包中手動啟動，消去 1 次黑歷史違規紀錄。", "type": "normal"},
        {"id": "item_05", "name": "📡 脈衝頻率干擾器", "price": 800, "desc": "【背包主動使用】可在公共頻道中發射一段嚴重受靜電雜訊干擾的扭曲廣播。", "type": "normal"},
        {"id": "rank_up_01", "name": "🎖️ 晉升：資深探員", "price": 1000, "desc": "身分正式從【菜鳥特工】晉升為【資深探員】", "type": "rank", "target_rank": "資深探員", "required_rank": "菜鳥特工"},
        {"id": "rank_up_02", "name": "👑 晉升：王牌特工", "price": 3000, "desc": "身分正式從【資深探員】晉升為【王牌特工】", "type": "rank", "target_rank": "王牌特工", "required_rank": "資深探員"},
        {"id": "rank_up_03", "name": "👻 晉升：幽靈傳器", "price": 6000, "desc": "身分正式從【王牌特工】晉升為【幽靈傳奇】", "type": "rank", "target_rank": "幽靈傳奇", "required_rank": "王牌特工"},
        {"id": "rank_up_04", "name": "👥 晉升：影子特工", "price": 12000, "desc": "踏入核心陰影，晉升為【影子特工】，解鎖調查檔案存取權。", "type": "rank", "target_rank": "影子特工", "required_rank": "幽靈傳奇"},
        {"id": "rank_up_05", "name": "⚖️ 晉升：天網審判官", "price": 25000, "desc": "天網最高榮譽階級【天網審判官】，象徵絕對統治實力。", "type": "rank", "target_rank": "天網審判官", "required_rank": "影子特工"}
    ]

# 初始化基礎檔案
DEFAULT_ADMIN = {"agent_alpha": "alpha7788"}
if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) < 5:
    DataManager.save(USERS_FILE, [{"user": "agent_007", "pwd": "pwd7788", "status": "active", "created_at": "2026-01-01 00:00:00", "failed_count": 0, "points": 1000, "rank": "菜鳥特工", "inventory": {}, "holdings": {}}])

if not os.path.exists(SHOP_FILE) or os.path.getsize(SHOP_FILE) < 500:
    DataManager.save(SHOP_FILE, get_default_shop_items())

sys_config = DataManager.load(CONFIG_FILE)
if not sys_config:
    sys_config = {"fake_lock": False}
    DataManager.save(CONFIG_FILE, sys_config)

# 初始化金融市場價格
market_rates = DataManager.load(MARKET_FILE)
if not market_rates or "SKY" not in market_rates:
    market_rates = {
        "SKY": {"name": "天網幣 (SKY)", "rate": 10.0, "history": [10.0]},
        "SHDW": {"name": "影網資訊 (SHDW)", "rate": 45.0, "history": [45.0]},
        "MEGA": {"name": "巨型科技 (MEGA)", "rate": 120.0, "history": [120.0]},
        "NANO": {"name": "奈米生化 (NANO)", "rate": 80.0, "history": [80.0]}
    }
    DataManager.save(MARKET_FILE, market_rates)


# --- 5. 模擬動態匯率波動更新 ---
def tick_market_prices():
    """
    動態更新期貨市場行情，每次重載隨機微調，並儲存歷史紀錄以便畫線
    """
    global market_rates
    updated = False
    for asset_id, info in market_rates.items():
        current_price = info.get("rate", 10.0)
        change_pct = random.uniform(-0.25, 0.30)
        new_price = round(max(1.0, current_price * (1 + change_pct)), 2)
        
        info["rate"] = new_price
        hist = info.get("history", [])
        hist.append(new_price)
        info["history"] = hist[-10:]
        updated = True
        
    if updated:
        DataManager.save(MARKET_FILE, market_rates)


# --- 6. 賽博龐克圖形解鎖與身份認證系統 ---
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.update({"authenticated": False, "user": None, "click_count": 0, "show_secret_panel": False})
    if st.session_state["authenticated"]:
        return True
    
    current_config = DataManager.load(CONFIG_FILE)

    st.markdown("""
        <div style='background: radial-gradient(circle, #081024 0%, #010408 100%); padding: 30px; border-radius: 12px; border: 2px solid #39ff14; box-shadow: 0 0 30px rgba(57, 255, 20, 0.4); text-align: center; margin-bottom: 25px;'>
            <h1 style='color: #39ff14; text-shadow: 0 0 15px #39ff14; font-size: 2.8em;'>🛡️ SKYNET LEGENDARY TERMINAL</h1>
            <p style='color: #00ffcc; font-weight: bold; font-size: 1.1em;' class='neon-blink'>[中央安全防火陣列 - 權限稽核與生物驗證層]</p>
        </div>
    """, unsafe_allow_html=True)

    col_space1, col_btn, col_space2 = st.columns([1.8, 1.2, 1.8])
    with col_btn:
        st.write("")
        st.markdown("<p style='text-align:center; color:#00ffcc; font-size:12px; margin-bottom:-5px;'>[ CENTRAL CORE GATEWAY ]</p>", unsafe_allow_html=True)
        if st.button("🟢\n\n⚡️ SKYNET CORE GATEWAY ⚡️\n\n🟢", key="hidden_image_trigger", use_container_width=True):
            st.session_state["click_count"] += 1
            if st.session_state["click_count"] >= 3:
                st.session_state["show_secret_panel"] = True  
                st.session_state["click_count"] = 0
                st.rerun()

    if st.session_state["show_secret_panel"]:
        st.markdown("""
            <div style='border: 1px dashed #ff9900; background-color: rgba(255, 153, 0, 0.1); padding: 15px; border-radius: 10px; margin: 20px 0;'>
                <h3 style='color: #ff9900; text-align: center; text-shadow: 0 0 5px #ff9900;'>🛰️ 發現應急強制重置後門通道</h3>
            </div>
        """, unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1.5, 2, 1.5])
        with col_c2:
            with st.container(border=True):
                st.write("點擊下方應急控制按鈕可直接強制清除防禦牆限流（解封鎖）。")
                if st.button("🔓 強制解除假封鎖狀態", key="true_unlock_image_btn", use_container_width=True):
                    current_config["fake_lock"] = False
                    DataManager.save(CONFIG_FILE, current_config)
                    log_activity("應急通道：探員強制清除中央防禦鎖定狀態", "核心應急探針")
                    st.session_state["show_secret_panel"] = False
                    st.success("🎉 假封鎖已被清除！天網通道完全通暢。")
                    st.rerun()
                if st.button("關閉應急終端", use_container_width=True):
                    st.session_state["show_secret_panel"] = False
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    mode = st.radio("驗證身分模式", ["登入系統", "申請探員註冊"], horizontal=True, label_visibility="collapsed")
    
    if mode == "登入系統":
        u = st.text_input("📁 探員識別碼 (ID)", key="login_uid")
        p = st.text_input("🔑 安全授權碼 (ACCESS PASS)", type="password", key="login_pwd")
        if st.button("🔐 執行身分安全認證", use_container_width=True, type="primary"):
            if u in DEFAULT_ADMIN and DEFAULT_ADMIN[u] == p:
                st.session_state.update({"authenticated": True, "user": u})
                st.rerun()
            
            if current_config.get("fake_lock", False):
                st.markdown("<p style='color: #ffaa00; font-weight: bold; text-align: center;'>❌ 連線阻斷：中央防火牆正處於防禦封鎖狀態。 (ERR_SKYNET_SHIELD_ACTIVE)</p>", unsafe_allow_html=True)
                return False
                
            users = DataManager.load(USERS_FILE)
            user = next((x for x in users if x.get("user") == u and x.get("pwd") == p), None)
            if user and user.get("status") == "active":
                st.session_state.update({"authenticated": True, "user": u})
                log_activity("登入系統", u)
                st.rerun()
            else:
                st.error("認證比對失敗，或該特工代號尚未通過最高指揮部審核啟用。")
    else:
        if current_config.get("fake_lock", False):
            st.error("🚨 警告：全網假防禦鎖定中，暫停一切新成員簽核。")
            return False
            
        new_u = st.text_input("🔒 創立新識別碼", key="reg_uid")
        new_p = st.text_input("🔑 設定安全授權碼", type="password", key="reg_pwd")
        if st.button("📤 提交特工註冊審批", use_container_width=True):
            if not new_u or not new_p:
                st.error("核心註冊資訊不可留空！")
                return False
            users = DataManager.load(USERS_FILE)
            if any(x.get("user") == new_u for x in users) or new_u in DEFAULT_ADMIN:
                st.error("該識別碼已被天網資料庫註記註冊。")
            else:
                reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                users.append({
                    "user": new_u, "pwd": new_p, "status": "pending", "created_at": reg_time,
                    "failed_count": 0, "points": 0, "rank": "菜鳥特工", "inventory": {}, "holdings": {}
                })
                DataManager.save(USERS_FILE, users)
                st.success("📝 遞交成功！請静候指揮官批准並活化您的特工識別碼。")
    return False


# --- 7. 核心主程式邏輯 ---
if authenticate():
    current_agent = st.session_state["user"]
    is_admin = (current_agent == "agent_alpha")
    
    sys_config = DataManager.load(CONFIG_FILE)
    if sys_config.get("fake_lock", False) and not is_admin:
        st.markdown("<h2 style='color:#ffaa00; text-align:center;'>🚨 最高警報：天網目前假封鎖中</h2>", unsafe_allow_html=True)
        st.error("指揮部已暫停普通特工終端通行的連線能力。請稍後重試。")
        st.stop()

    tick_market_prices()

    # 原子加載全局資料
    tasks = DataManager.load(DB_FILE)
    chats = DataManager.load(CHAT_FILE)
    users = DataManager.load(USERS_FILE)
    shop_items = DataManager.load(SHOP_FILE)
    private_chats = DataManager.load(PRIVATE_CHAT_FILE)
    invest_data = DataManager.load(INVEST_FILE)

    u_data = next((u for u in users if u.get("user") == current_agent), None)
    pts = u_data.get("points", 0) if u_data else (999999 if is_admin else 0)
    rank = u_data.get("rank", "菜鳥特工") if u_data else ("最高指揮官" if is_admin else "快捷探員")

    # 側邊欄改版：動態雷達與背包物品使用介面
    st.sidebar.markdown("""
        <div style='background-color:#020612; padding:15px; border-radius:10px; border:1px solid #39ff14; text-align:center; margin-bottom:15px;'>
            <span style='color:#39ff14; font-size:1.2em; font-weight:bold; text-shadow: 0 0 5px #39ff14;'>🛰️ 特工信道連線</span><br>
            <span style='color:#39ff14;' class='neon-blink'>🟢 ENCRYPTED ONLINE</span>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.info(f"**👤 特工識別:** {current_agent}\n\n**🎖️ 天網階級:** `{rank}`\n\n**💰 帳戶餘額:** `{pts}` PTS\n\n**❌ 違規黑歷史:** `{u_data.get('failed_count', 0) if u_data else 0} / 3` 次")
    
    # --- 側邊欄背包：實體化道具使用功能 ---
    if u_data:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎒 特工個人背包 (可主動點擊使用)")
        inv = u_data.get("inventory", {})
        
        # 🧪 奈米修復血清的使用
        serum_count = inv.get("item_04", 0)
        col_serum1, col_serum2 = st.sidebar.columns([2, 1])
        with col_serum1:
            st.markdown(f"🧪 奈米修復血清: `{serum_count}` 個")
        with col_serum2:
            if st.button("使用", key="use_item_04", disabled=(serum_count < 1)):
                u_data["inventory"]["item_04"] -= 1
                if u_data["failed_count"] > 0:
                    u_data["failed_count"] -= 1
                    play_synth_sound("beep")
                    st.toast("🧪 血清修復完成！違規次數已消除 1 次！", icon="🧪")
                else:
                    st.toast("🧪 血清已消耗，未進行任何違規次數扣減。", icon="🧪")
                DataManager.save(USERS_FILE, users)
                log_activity("於背包中啟用了【奈米修復血清】", current_agent)
                time.sleep(0.5)
                st.rerun()

        # 📡 脈衝頻率干擾器的使用
        jammer_count = inv.get("item_05", 0)
        col_jam1, col_jam2 = st.sidebar.columns([2, 1])
        with col_jam1:
            st.markdown(f"📡 脈衝干擾器: `{jammer_count}` 個")
        with col_jam2:
            if "show_jammer_input" not in st.session_state:
                st.session_state["show_jammer_input"] = False
            if st.button("發動", key="use_item_05_btn", disabled=(jammer_count < 1)):
                st.session_state["show_jammer_input"] = not st.session_state["show_jammer_input"]
                
        if st.session_state["show_jammer_input"] and jammer_count > 0:
            jam_text = st.sidebar.text_input("輸入欲干擾的廣播文字", placeholder="例如: 天網已被離線")
            if st.sidebar.button("確認釋放脈衝"):
                if jam_text:
                    u_data["inventory"]["item_05"] -= 1
                    distorted_chars = ["%", "$", "@", "*", "#", "!", "X", "Z", "⚡", "📶", "🛸"]
                    distorted_text = "".join([char if random.random() > 0.4 else random.choice(distorted_chars) for char in jam_text])
                    chats.append({"time": datetime.now().strftime("%M:%S"), "sender": f"⚠️ 頻率干擾 [{current_agent}]", "text": f"[脈衝強行寫入] ── {distorted_text}"})
                    DataManager.save(CHAT_FILE, chats)
                    DataManager.save(USERS_FILE, users)
                    log_activity("使用【脈衝干擾器】向公共信道發布了強干擾訊息", current_agent)
                    st.session_state["show_jammer_input"] = False
                    play_synth_sound("static")
                    st.toast("📡 脈衝波發射成功！廣播頻道信道已被靜電波扭曲！", icon="📡")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.sidebar.error("請輸入干擾文字。")

    if st.sidebar.button("🚪 安全切斷戰情終端", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    # 高科技十一頁籤
    tabs = st.tabs([
        "📋 任務大廳", "➕ 發布任務", "⚔️ 戰情回報", "📸 視訊面部掃描",
        "🛸 無人機探勘", "📈 金融期貨交易所", "🏆 特工榜單", "🏪 黑市商店",
        "📡 訊號傳譯器", "📢 廣播頻道", "🔐 私密通訊", "📂 調查線索庫",
        "👑 指揮中心"
    ])

    with tabs[0]: # 任務大廳
        st.subheader("📋 探員戰術懸賞告示")
        available_tasks = [t for t in tasks if t.get("status") == "待接取" and t.get("posted_by") != current_agent]
        if not available_tasks:
            st.info("當前雷達範圍無活動中的懸賞任務。")
        for t in available_tasks:
            st.markdown(f"""
                <div style='background-color:#050c18; border:1px solid #39ff14; padding:15px; border-radius:8px; margin: 10px 0;'>
                    <span style='color:#39ff14; font-size:1.3em; font-weight:bold; text-shadow: 0 0 3px #39ff14;'>🎯 {t.get('task_name')}</span> |
                    <span style='color:#00ffcc; font-weight:bold;'>💰 託管賞金: {t.get('reward', 0)} PTS</span><br>
                    <span style='color:#888;'>發起特工: {t.get('posted_by', '天網系統')}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🎯 接取並下載戰術指令", key=f"ac_{t.get('id')}"):
                t.update({"status": "已接取", "accepted_by": current_agent})
                DataManager.save(DB_FILE, tasks)
                st.toast("任務接取成功！", icon="🎯")
                time.sleep(0.5)
                st.rerun()

    with tabs[1]: # 發布任務
        st.subheader("➕ 發布全新戰術懸賞令")
        with st.form("post_task_form"):
            n = st.text_input("📝 任務目標 / 情報描述")
            r = st.number_input("💰 託管賞金 (PTS)", min_value=1, value=100, step=50)
            if st.form_submit_button("📢 封鎖賞金並發布廣播"):
                if not n:
                    st.error("必須填寫任務目標說明。")
                elif not is_admin and pts < r:
                    st.error("您個人餘額不足，無法託管賞金。")
                else:
                    if u_data:
                        u_data["points"] -= r
                        DataManager.save(USERS_FILE, users)
                    tasks.append({"id": str(int(datetime.now().timestamp())), "task_name": n, "reward": r, "status": "待接取", "posted_by": current_agent})
                    DataManager.save(DB_FILE, tasks)
                    log_activity(f"發布了新懸賞任務: {n}", current_agent)
                    st.success("懸賞令發布成功！已向全網進行廣播。")
                    time.sleep(0.5)
                    st.rerun()

    with tabs[2]: # 戰情中心
        st.subheader("⚔️ 指令進度與回報審批")
        my_posted_need_review = [t for t in tasks if t.get("posted_by") == current_agent and t.get("status") == "等待審核"]
        my_accepted_tasks = [t for t in tasks if t.get("accepted_by") == current_agent and t.get("status") == "已接取"]
        
        if my_accepted_tasks:
            st.markdown("#### ⏳ 您承接中的行動任務")
            for t in my_accepted_tasks:
                with st.container(border=True):
                    st.write(f"**目標:** {t.get('task_name')} | **酬金:** {t.get('reward')} PTS")
                    if st.button("📤 提交最終執行成果", key=f"report_{t.get('id')}"):
                        t["status"] = "等待審核"
                        DataManager.save(DB_FILE, tasks)
                        st.success("成果報告已加密上報，等待審核。")
                        time.sleep(0.5)
                        st.rerun()

        if my_posted_need_review:
            st.markdown("#### 🔔 待您核准的特工成果報告")
            for nt in my_posted_need_review:
                with st.container(border=True):
                    st.warning(f"特工 **{nt.get('accepted_by')}** 已上傳回報： {nt.get('task_name')}")
                    if st.button("👍 審查通過，解除賞金託管", key=f"y_{nt.get('id')}"):
                        nt["status"] = "已完成"
                        target = next((u for u in users if u.get("user") == nt.get("accepted_by")), None)
                        if target:
                            target["points"] = target.get("points", 0) + nt.get("reward", 0)
                        DataManager.save(USERS_FILE, users)
                        DataManager.save(DB_FILE, tasks)
                        log_activity(f"審核通過特工 {nt.get('accepted_by')} 的任務回報", current_agent)
                        st.success("審批完成，PTS 積分已自動匯入對方特工帳戶。")
                        time.sleep(0.5)
                        st.rerun()
        
        if not my_accepted_tasks and not my_posted_need_review:
            st.info("當前沒有承接任何行動，亦無等待審查的回報進度。")

    with tabs[3]: # 📸 視訊面部掃描 & 模擬滲透
        st.subheader("📸 實時視訊與虛擬身分演練")
        use_privacy_mask = st.checkbox("🔮 啟動天網「虛擬身分遮罩協定」 (不露臉/加密虛擬矩陣模式)", value=is_admin)
        
        camera_image = None
        ready_to_simulate = False
        
        if not use_privacy_mask:
            st.markdown("<p style='color:#39ff14;'>[請注視鏡頭，保持靜止，執行面部網格映射...]</p>", unsafe_allow_html=True)
            camera_image = st.camera_input("📡 啟動實時面部識別驗證掃描")
            if camera_image:
                st.toast("🟢 實時視訊網格映射完成！特徵資料已完成對齊。", icon="🟢")
                ready_to_simulate = True
                img_bytes = camera_image.getvalue()
                with open(os.path.join(IMAGE_DIR, f"{current_agent}_face.png"), "wb") as f:
                    f.write(img_bytes)
        else:
            st.markdown("""
                <div style='background-color:rgba(57,255,20,0.05); padding:15px; border-radius:8px; border:1px solid #39ff14; margin-bottom:15px;'>
                    <span style='color:#39ff14; font-weight:bold;'>[🛡️ SKYNET ANONYMOUS MASK ACTIVE]</span><br>
                    已動態生成 1024-bit 假實體雜湊面部網格。本機鏡頭已關閉。
                </div>
            """, unsafe_allow_html=True)
            ready_to_simulate = True

        st.divider()
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.write("### 🎲 身份特徵演練")
            has_key = u_data.get("inventory", {}).get("item_01", 0) > 0 if u_data else False
            has_sat = u_data.get("inventory", {}).get("item_02", 0) > 0 if u_data else False
            has_cloak = u_data.get("inventory", {}).get("item_03", 0) > 0 if u_data else False
            
            st.markdown("##### ⚡ 載入滲透支援道具")
            use_item_01 = st.checkbox(f"🔑 進階解密金鑰 (可用: {u_data.get('inventory', {}).get('item_01', 0) if u_data else 0} ) ➔ 成功率額外 +30%", disabled=not has_key)
            use_item_02 = st.checkbox(f"🛰️ 衛星追蹤權限 (可用: {u_data.get('inventory', {}).get('item_02', 0) if u_data else 0} ) ➔ 積分獲利雙倍 (x2)", disabled=not has_sat)
            use_item_03 = st.checkbox(f"🧥 匿蹤防護斗篷 (可用: {u_data.get('inventory', {}).get('item_03', 0) if u_data else 0} ) ➔ 失敗免除懲罰", disabled=not has_cloak)
            
            base_success = 45
            final_success = base_success + (30 if use_item_01 else 0)
            st.markdown(f"**💡 最終預估成功機率： `{final_success}%`**")
            
            if st.button("🔥 啟動虛擬模擬滲透", type="primary", use_container_width=True, disabled=not ready_to_simulate):
                if use_item_01: u_data["inventory"]["item_01"] -= 1
                if use_item_02: u_data["inventory"]["item_02"] -= 1
                if use_item_03: u_data["inventory"]["item_03"] -= 1
                
                dice = random.randint(1, 100)
                if dice <= final_success:
                    base_reward = random.randint(300, 800)
                    win = base_reward * (2 if use_item_02 else 1)
                    if u_data:
                        u_data["points"] = u_data.get("points", 0) + win
                    st.success(f"🟢 演練成功！完美突入防禦節點，獲得了 {win} PTS 酬勞！")
                    log_activity(f"動態演練滲透成功，獲得了 {win} PTS", current_agent)
                else:
                    st.error("🔴 演練失敗！虛擬特徵遭系統反噬。")
                    if use_item_03:
                        st.warning("🧥 已檢測到匿蹤防護斗篷。已阻斷敵方天網反向追蹤，免除違規紀錄處罰！")
                        log_activity("動態演練失敗，使用了防護斗篷免疫處罰", current_agent)
                    else:
                        if u_data:
                            u_data["failed_count"] = u_data.get("failed_count", 0) + 1
                            if u_data["failed_count"] >= 3:
                                users = [u for u in users if u.get("user") != current_agent]
                                DataManager.save(USERS_FILE, users)
                                st.error("💀 違規紀錄達 3 次！特工終端已被天網永久抹除。")
                                log_activity(f"因違規達3次，特工帳戶已遭物理抹除: {current_agent}", "系統")
                                st.session_state.authenticated = False
                                time.sleep(1.5)
                                st.rerun()
                        st.error("系統違規次數已增加。")
                DataManager.save(USERS_FILE, users)
                time.sleep(1)
                st.rerun()
            if not ready_to_simulate:
                st.info("💡 請先開啟視訊鏡頭（Webcam）或啟用「虛擬身分遮罩協定」，即可解鎖演練按鈕。")

    with tabs[4]: # 🛸 無人機掛網探勘系統
        st.subheader("🛸 無人機遠程探勘派遣系統")
        st.caption("透過將特工無人機派遣至高危暗網網段，離線挂網即可自動探勘並收割豐富的 PTS 積分！")
        
        if not u_data:
            st.info("管理員帳號無須執行掛網探勘任務。")
        else:
            drone_mission = u_data.get("drone_dispatch", {})
            current_time = datetime.now()
            
            if drone_mission:
                end_time = datetime.strptime(drone_mission["end_time"], "%Y-%m-%d %H:%M:%S")
                if current_time >= end_time:
                    st.success(f"🟢 派遣完成！無人機已從網段 **【{drone_mission['target_name']}】** 返航！")
                    st.markdown(f"📦 成功取回加密封包，解密後獲得： **+{drone_mission['reward']} PTS**")
                    if st.button("🛸 收回無人機並結算積分", use_container_width=True):
                        u_data["points"] = u_data.get("points", 0) + drone_mission['reward']
                        u_data["drone_dispatch"] = {}
                        DataManager.save(USERS_FILE, users)
                        log_activity(f"無人機探勘回收，獲得 {drone_mission['reward']} PTS", current_agent)
                        play_synth_sound("beep")
                        st.success("積分結算成功！無人機整備中。")
                        time.sleep(1)
                        st.rerun()
                else:
                    time_left = end_time - current_time
                    st.info(f"⏳ 無人機正在網段 **【{drone_mission['target_name']}】** 進行深層解密中...")
                    st.metric("剩餘探勘時間", f"{time_left.seconds // 60} 分 {time_left.seconds % 60} 秒")
                    st.progress(min(1.0, 1.0 - (time_left.total_seconds() / drone_mission['total_duration'])))
                    if st.button("🛸 緊急召回無人機 (不回收積分且無法退還出資)", use_container_width=True):
                        u_data["drone_dispatch"] = {}
                        DataManager.save(USERS_FILE, users)
                        log_activity("緊急撤回了無人機探勘任務", current_agent)
                        st.warning("無人機已強行斷開返回。")
                        time.sleep(1)
                        st.rerun()
            else:
                st.markdown("#### 選擇探勘派遣目標")
                col_d1, col_d2, col_d3 = st.columns(3)
                
                targets = [
                    {"name": "Subnet-Alpha (初級)", "cost": 100, "reward": 250, "duration": 60},
                    {"name": "Deep-Vault-Beta (中級)", "cost": 300, "reward": 750, "duration": 180},
                    {"name": "Orion-Core-Zero (高危)", "cost": 600, "reward": 1800, "duration": 360}
                ]
                
                for idx, t in enumerate(targets):
                    with [col_d1, col_d2, col_d3][idx]:
                        with st.container(border=True):
                            st.write(f"🌐 **{t['name']}**")
                            st.write(f"· 出資成本: `{t['cost']} PTS`")
                            st.write(f"· 預估收益: `{t['reward']} PTS`")
                            st.write(f"· 派遣時長: `{t['duration']} 秒`")
                            if st.button(f"🚀 派遣至 {t['name'].split(' ')[0]}", key=f"drone_start_{idx}", disabled=(pts < t['cost'])):
                                u_data["points"] -= t['cost']
                                u_data["drone_dispatch"] = {
                                    "target_name": t['name'],
                                    "reward": t['reward'],
                                    "total_duration": t['duration'],
                                    "end_time": (datetime.now() + timedelta(seconds=t['duration'])).strftime("%Y-%m-%d %H:%M:%S")
                                }
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"派遣無人機前往 {t['name']}", current_agent)
                                play_synth_sound("beep")
                                st.success("無人機發射升空！信道切換至背景異步作業。")
                                time.sleep(1)
                                st.rerun()

    with tabs[5]: # 📈 金融期貨交易所
        st.subheader("📈 天網多指標期貨交易所")
        st.caption("賽博世界的高風險產物。每當終端重載，全網走勢將發生激烈重組！")
        
        col_m1, col_m2 = st.columns([2, 3])
        with col_m1:
            st.markdown("#### 💹 當前實時看板")
            for asset_id, info in market_rates.items():
                hist = info.get("history", [info["rate"]])
                prev_price = hist[-2] if len(hist) > 1 else info["rate"]
                delta_val = round(info["rate"] - prev_price, 2)
                st.metric(label=info["name"], value=f"{info['rate']} PTS", delta=f"{delta_val} ({round((delta_val/max(1,prev_price))*100,1)}%)")
        
        with col_m2:
            st.markdown("#### 💼 倉位管理與資產對沖")
            if not u_data:
                st.info("管理員權限無法參與平民市場套利。")
            else:
                holdings = u_data.get("holdings", {})
                selected_asset = st.selectbox("選擇欲交易標的", list(market_rates.keys()), format_func=lambda x: market_rates[x]["name"])
                
                current_rate = market_rates[selected_asset]["rate"]
                my_qty = holdings.get(selected_asset, 0)
                
                st.write(f"· 您當前持倉量: `{my_qty}` 單位")
                
                col_trade1, col_trade2 = st.columns(2)
                with col_trade1:
                    buy_amt = st.number_input("買入數量", min_value=1, value=1, step=1, key="buy_qty_in")
                    if st.button("🟢 執行多頭委託買入", use_container_width=True):
                        total_cost = round(buy_amt * current_rate, 2)
                        if pts >= total_cost:
                            u_data["points"] = round(u_data["points"] - total_cost, 2)
                            u_data["holdings"][selected_asset] = holdings.get(selected_asset, 0) + buy_amt
                            DataManager.save(USERS_FILE, users)
                            log_activity(f"買入 {buy_amt} 單位 {selected_asset}", current_agent)
                            st.success(f"交割成功！扣除 {total_cost} PTS。")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("流動性餘額不足，委託單遭拒。")
                with col_trade2:
                    sell_amt = st.number_input("賣出數量", min_value=1, max_value=max(1, my_qty), value=1, step=1, key="sell_qty_in")
                    if st.button("🔴 執行空頭清算賣出", use_container_width=True, disabled=(my_qty < 1)):
                        if my_qty >= sell_amt:
                            total_gain = round(sell_amt * current_rate, 2)
                            u_data["points"] = round(u_data["points"] + total_gain, 2)
                            u_data["holdings"][selected_asset] -= sell_amt
                            DataManager.save(USERS_FILE, users)
                            log_activity(f"清算賣出 {sell_amt} 單位 {selected_asset}", current_agent)
                            st.success(f"清算成功！入帳 {total_gain} PTS。")
                            time.sleep(0.5)
                            st.rerun()

    with tabs[6]: # 🏆 特工榜單
        st.subheader("🏆 全網特工戰力天梯榜")
        scouted_agents = [{"特工識別碼": x.get("user"), "天網階級": x.get("rank"), "資產(PTS)": x.get("points"), "安全狀態": "正常" if x.get("status")=="active" else "封印中"} for x in users]
        if scouted_agents:
            df_leader = pd.DataFrame(scouted_agents).sort_values(by="資產(PTS)", ascending=False).reset_index(drop=True)
            st.table(df_leader)

    with tabs[7]: # 🏪 黑市商店
        st.subheader("🏪 矩陣黑市補給站")
        col_s_idx = 0
        columns_shop = st.columns(3)
        for item in shop_items:
            with columns_shop[col_s_idx % 3]:
                with st.container(border=True):
                    st.markdown(f"##### {item.get('name')}")
                    st.write(f"價格: `{item.get('price')}` PTS")
                    st.caption(item.get('desc'))
                    
                    # 判斷按鈕狀態
                    can_buy = True
                    btn_label = "🛒 支付積分扣款"
                    if not u_data:
                        can_buy = False
                    else:
                        if item.get("type") == "rank":
                            if rank == item.get("target_rank"):
                                can_buy = False
                                btn_label = "✅ 已擁有此階級"
                            elif rank != item.get("required_rank"):
                                can_buy = False
                                btn_label = f"🔒 需先取得 {item.get('required_rank')}"
                        if pts < item.get("price") and can_buy:
                            can_buy = False
                            btn_label = "❌ PTS 餘額不足"
                            
                    if st.button(btn_label, key=f"buy_{item.get('id')}", disabled=not can_buy):
                        u_data["points"] -= item.get("price")
                        if item.get("type") == "rank":
                            u_data["rank"] = item.get("target_rank")
                            log_activity(f"在黑市將權限正式晉升至 【{item.get('target_rank')}】", current_agent)
                        else:
                            inv = u_data.get("inventory", {})
                            inv[item.get("id")] = inv.get(item.get("id"), 0) + 1
                            u_data["inventory"] = inv
                            log_activity(f"在黑市購買了補給道具: {item.get('name')}", current_agent)
                        
                        DataManager.save(USERS_FILE, users)
                        play_synth_sound("beep")
                        st.success(f"🎉 成功解鎖購入 {item.get('name')}！")
                        time.sleep(0.5)
                        st.rerun()
            col_s_idx += 1

    with tabs[8]: # 📡 訊號傳譯器
        st.subheader("📡 全球加密訊號變頻調製器")
        mode_m = st.radio("模式設定", ["摩斯編碼化 (Encrypt)", "摩斯解碼化 (Decrypt)"], horizontal=True)
        t_in = st.text_area("輸入原始密文段落", placeholder="Enter text or morse code here...")
        if st.button("⚡ 執行異步調製轉換"):
            if t_in:
                if mode_m == "摩斯編碼化 (Encrypt)":
                    st.code(encrypt_morse(t_in), language="markdown")
                else:
                    st.code(decrypt_morse(t_in), language="markdown")
            else:
                st.error("未偵測到任何可傳譯的訊號字元。")

    with tabs[9]: # 📢 廣播頻道（公用聊天室）
        st.subheader("📢 全網公共公鑰通訊廣播信道")
        st.caption("警告：此信道未進行端到端匿名分流，所有探員皆可即時接收並檢視此處的動態擴音。")
        
        # 顯示歷史廣播訊息
        chat_container = st.container(height=300, border=True)
        with chat_container:
            if not chats:
                st.markdown("<p style='color:#666;'>[目前信道靜默中，暫無公共廣播]</p>", unsafe_allow_html=True)
            for c in chats:
                # 兼容舊格式若無時間戳
                t_str = f"[{c['time']}] " if "time" in c else ""
                st.markdown(f"📡 **{t_str}{c.get('sender')}** : {c.get('text')}")
                
        # 發送廣播
        with st.form("public_chat_form", clear_on_submit=True):
            pub_msg = st.text_input("📤 發射廣播訊號 (Text Input)", placeholder="輸入想擴音至全網的戰術訊息...")
            if st.form_submit_button("確認發射廣播"):
                if pub_msg.strip():
                    chats.append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "sender": f"{current_agent} ({rank})",
                        "text": pub_msg
                    })
                    DataManager.save(CHAT_FILE, chats)
                    log_activity("向公用公共廣播信道發送了訊息", current_agent)
                    st.rerun()
                else:
                    st.error("廣播內文字元數不得為空。")

    with tabs[10]: # 🔐 私密通訊（定向私訊）
        st.subheader("🔐 端到端多節點分流私密通道")
        st.caption("天網雙向加密點對點傳輸協定，僅有指定的目標特工發送與接收端可解鎖該通訊聯動。")
        
        # 取得系統中所有可通訊的特工代號
        all_agents = [x.get("user") for x in users] + list(DEFAULT_ADMIN.keys())
        all_agents = [agent for agent in all_agents if agent != current_agent] # 排除自己
        
        if not all_agents:
            st.info("當前雷達網段中未發現其他可連線的活耀特工識別碼。")
        else:
            target_receiver = st.selectbox("🎯 定向指定目標特工代號 (Receiver ID)", all_agents)
            
            # 讀取並過濾出與該特工相關的私密對話
            st.markdown(f"##### 🛰️ 與 特工 `[{target_receiver}]` 的專屬加密信道")
            private_container = st.container(height=250, border=True)
            
            with private_container:
                # 過濾出彼此的對話
                conv = [m for m in private_chats if 
                        (m.get("sender") == current_agent and m.get("receiver") == target_receiver) or
                        (m.get("sender") == target_receiver and m.get("receiver") == current_agent)]
                
                if not conv:
                    st.markdown("<p style='color:#666;'>[信道已安全對齊，尚無任何通訊紀錄，請啟動首次通訊]</p>", unsafe_allow_html=True)
                for m in conv:
                    t_str = f"[{m['time']}] " if "time" in m else ""
                    if m.get("sender") == current_agent:
                        st.markdown(f"🟢 **{t_str}您** 发送给 **{target_receiver}**: {m.get('text')}")
                    else:
                        st.markdown(f"🔵 **{t_str}特工 [{target_receiver}]**: {m.get('text')}")
            
            # 發送私訊表單
            with st.form("private_chat_form", clear_on_submit=True):
                priv_msg = st.text_input("🔒 寫入高強度加密字串", placeholder=f"傳送私密戰術代碼給 {target_receiver}...")
                if st.form_submit_button("傳送加密私訊"):
                    if priv_msg.strip():
                        private_chats.append({
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "sender": current_agent,
                            "receiver": target_receiver,
                            "text": priv_msg
                        })
                        DataManager.save(PRIVATE_CHAT_FILE, private_chats)
                        log_activity(f"對特工 {target_receiver} 發起端到端私密通訊", current_agent)
                        st.rerun()
                    else:
                        st.error("密訊內容不得為留空。")

    with tabs[11]: # 📂 調查線索庫
        st.subheader("📂 國家級絕密調查情報檔案庫")
        if rank not in ["影子特工", "天網審判官", "最高指揮官"] and not is_admin:
            st.error("🔒 權限階級封鎖！此線索庫需要【影子特工】或更高級別權限方可解鎖矩陣拷貝。")
            st.warning("提示：可以前往【黑市商店】升級您的特工授權階級。")
        else:
            st.success("🔓 驗證通過！已解鎖深層調查密檔。")
            st.markdown("""
                * **【線索 01 - 項目SKYNET原型機】** : 核心控制權限似乎存在一個由指揮官設置的應急後門，可透過在驗證網關連續點擊核心標誌 3 次強行觸發。
                * **【線索 02 - 暗網黑客代號】** : 傳聞常駐於本終端的 `agent_007` 帳號暗中掌握了極大一部分的早期技術積分。
                * **【線索 03 - 脈衝干擾原理】** : 利用特定高周波可直接向廣播終端注入污染噪聲，能隱蔽自己的真實識別痕跡。
            """)

    with tabs[12]: # 👑 指揮中心
        st.subheader("👑 中央天網核心控制台")
        if not is_admin:
            st.error("❌ 您不是最高指揮官(agent_alpha)，無權調閱中央防禦總閘。")
        else:
            st.success("🎯 歡迎回到核心，最高指揮官。")
            
            # 審批新特工
            st.markdown("#### 👤 待簽核特工資格申請")
            pending_users = [x for x in users if x.get("status") == "pending"]
            if not pending_users:
                st.info("目前無待審核的註冊探員申請。")
            for pu in pending_users:
                with st.container(border=True):
                    st.write(f"識別碼: **{pu.get('user')}** | 申請時間: {pu.get('created_at')}")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if st.button("✅ 批准加入並活化帳戶", key=f"app_{pu.get('user')}"):
                            pu["status"] = "active"
                            pu["points"] = 1000  # 給予初始啟動 PTS
                            DataManager.save(USERS_FILE, users)
                            log_activity(f"指揮官批准了 {pu.get('user')} 的註冊申請", "最高指揮官")
                            st.success(f"{pu.get('user')} 已正式加入天網。")
                            time.sleep(0.5)
                            st.rerun()
                    with col_p2:
                        if st.button("❌ 物理抹除該註冊提案", key=f"rej_{pu.get('user')}"):
                            users.remove(pu)
                            DataManager.save(USERS_FILE, users)
                            st.warning("已駁回並銷毀該註冊提案。")
                            time.sleep(0.5)
                            st.rerun()
            
            st.divider()
            # 假封鎖總開關控制
            st.markdown("#### 🛡️ 戰略防火牆防禦管制")
            current_lock_status = sys_config.get("fake_lock", False)
            st.write(f"當前防火牆防禦鎖定狀態： `{'🛑 全網隔離中 (Fake Lock Active)' if current_lock_status else '🟢 正常開通中'}`")
            
            if current_lock_status:
                if st.button("🔓 關閉全網防禦牆 (恢復普通特工連線權利)", type="primary"):
                    sys_config["fake_lock"] = False
                    DataManager.save(CONFIG_FILE, sys_config)
                    log_activity("指揮官關閉了全網防禦鎖定", "最高指揮官")
                    st.rerun()
            else:
                if st.button("🚨 啟動極限假防禦隔離牆 (阻斷所有普通特工連線)"):
                    sys_config["fake_lock"] = True
                    DataManager.save(CONFIG_FILE, sys_config)
                    log_activity("指揮官啟動了全網假隔離牆防禦", "最高指揮官")
                    st.rerun()
                    
            st.divider()
            # 查看審計日誌
            st.markdown("#### 📑 終端中央安全審計日誌 (最新100條)")
            system_logs = DataManager.load(LOG_FILE)
            if system_logs:
                st.dataframe(pd.DataFrame(system_logs), use_container_width=True)
            else:
                st.info("暫無任何操作審計紀錄。")