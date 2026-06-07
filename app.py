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
        # 簡單的 1000Hz 嗶嗶聲 (WAV 格式 base64)
        audio_b64 = "UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQgAAAAAAAAA"
    elif sound_type == "static":
        # 靜電噪音/干擾聲模擬
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
MARKET_FILE = "market_rates.json" # 新增：天網期貨市場資料庫

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
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
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
        {"id": "rank_up_03", "name": "👻 晉升：幽靈傳奇", "price": 6000, "desc": "身分正式從【王牌特工】晉升為【幽靈傳奇】", "type": "rank", "target_rank": "幽靈傳奇", "required_rank": "王牌特工"},
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
        # 賽博金融：-25% 到 +30% 的高槓桿波動
        change_pct = random.uniform(-0.25, 0.30)
        new_price = round(max(1.0, current_price * (1 + change_pct)), 2)
        
        info["rate"] = new_price
        hist = info.get("history", [])
        hist.append(new_price)
        info["history"] = hist[-10:] # 只保留最新 10 次波動趨勢
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

    # 賽博龐克高科技終端面板
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
        # 動態點擊 3 次徽章圖片按鈕
        if st.button("🟢\n\n⚡️ SKYNET CORE GATEWAY ⚡️\n\n🟢", key="hidden_image_trigger", use_container_width=True):
            st.session_state["click_count"] += 1
            if st.session_state["click_count"] >= 3:
                st.session_state["show_secret_panel"] = True  
                st.session_state["click_count"] = 0
                st.rerun()

    # 隱藏的指揮官應急通道
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

    # 模擬隨機金融市場跳動
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
                    chats.append({"sender": f"⚠️ 頻率干擾 [{current_agent}]", "text": f"[脈衝強行寫入] ── {distorted_text}"})
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
            # 是否擁有並啟用道具
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
                # 扣除使用的滲透道具
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

    with tabs[4]: # 🛸 【全新功能】無人機掛網探勘系統
        st.subheader("🛸 無人機遠程探勘派遣系統")
        st.caption("透過將特工無人機派遣至高危暗網網段，離線挂網即可自動探勘並收割豐富的 PTS 積分！")
        
        if not u_data:
            st.info("管理員帳號無須執行掛網探勘任務。")
        else:
            drone_mission = u_data.get("drone_dispatch", {})
            current_time = datetime.now()
            
            # 檢查是否有正在進行的任務
            if drone_mission:
                end_time = datetime.strptime(drone_mission["end_time"], "%Y-%m-%d %H:%M:%S")
                if current_time >= end_time:
                    # 任務已完成，可以回收
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
                    # 任務進行中
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
                # 無任務，可派遣
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
                                log_activity(f"派遣無人機至 {t['name']}", current_agent)
                                play_synth_sound("beep")
                                st.success("無人機已順利彈射發射！")
                                time.sleep(1)
                                st.rerun()

    with tabs[5]: # 📈 【全新功能】天網期貨與加密市場
        st.subheader("📈 天網區塊鏈加密與 PTS 期貨交易所")
        st.caption("使用您的 PTS 積分進行低買高賣的期貨操作！幣價與天網全局算力隨機連動。")
        
        # 顯示當前市場價格走勢卡片
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        for idx, (asset_id, info) in enumerate(market_rates.items()):
            with [col_m1, col_m2, col_m3, col_m4][idx]:
                with st.container(border=True):
                    hist = info.get("history", [10.0])
                    diff = hist[-1] - hist[-2] if len(hist) > 1 else 0.0
                    arrow = "🔺" if diff >= 0 else "🔻"
                    color_style = "color:#39ff14;" if diff >= 0 else "color:#ff3333;"
                    st.write(f"**{info['name']}**")
                    st.markdown(f"## {info['rate']} <span style='font-size:14px;{color_style}'>{arrow} {diff:+.2f}</span>", unsafe_allow_html=True)
                    st.line_chart(hist)
                    
        st.divider()
        
        if not u_data:
            st.info("管理員擁有無限積分，無須進行資產套利。")
        else:
            col_trade1, col_trade2 = st.columns(2)
            with col_trade1:
                st.markdown("#### 🛒 購買資產")
                trade_asset = st.selectbox("選擇要購入的資產", list(market_rates.keys()), format_func=lambda x: market_rates[x]["name"])
                current_rate = market_rates[trade_asset]["rate"]
                max_buy = int(pts // current_rate)
                
                qty_buy = st.number_input(f"購入數量 (當前單價: {current_rate} PTS / 最大可買 {max_buy} 單位)", min_value=1, max_value=max(1, max_buy), value=1)
                total_cost = round(qty_buy * current_rate, 2)
                st.write(f"預計消耗: `{total_cost}` PTS")
                
                if st.button("🟢 確認購入資產", use_container_width=True, disabled=(pts < total_cost)):
                    u_data["points"] -= total_cost
                    holdings = u_data.get("holdings", {})
                    holdings[trade_asset] = holdings.get(trade_asset, 0) + qty_buy
                    u_data["holdings"] = holdings
                    DataManager.save(USERS_FILE, users)
                    log_activity(f"購入了 {qty_buy} 單位 {trade_asset}", current_agent)
                    play_synth_sound("beep")
                    st.success(f"成功購入 {qty_buy} 單位 {market_rates[trade_asset]['name']}！")
                    time.sleep(1)
                    st.rerun()
                    
            with col_trade2:
                st.markdown("#### 💰 賣出持倉")
                my_holdings = u_data.get("holdings", {})
                active_holdings = {k: v for k, v in my_holdings.items() if v > 0}
                
                if not active_holdings:
                    st.info("📊 您的帳戶目前無任何資產持倉。")
                else:
                    sell_asset = st.selectbox("選擇要拋售的資產", list(active_holdings.keys()), format_func=lambda x: f"{market_rates[x]['name']} (持倉: {active_holdings[x]})")
                    current_rate_sell = market_rates[sell_asset]["rate"]
                    max_sell = active_holdings[sell_asset]
                    
                    qty_sell = st.number_input("賣出數量", min_value=1, max_value=max_sell, value=max_sell)
                    total_payout = round(qty_sell * current_rate_sell, 2)
                    st.write(f"預計回收: `+{total_payout}` PTS")
                    
                    if st.button("🔴 確認拋售資產", use_container_width=True):
                        u_data["points"] += total_payout
                        u_data["holdings"][sell_asset] -= qty_sell
                        DataManager.save(USERS_FILE, users)
                        log_activity(f"賣出了 {qty_sell} 單位 {sell_asset}", current_agent)
                        play_synth_sound("beep")
                        st.success(f"成功拋售並收回 {total_payout} PTS！")
                        time.sleep(1)
                        st.rerun()

    with tabs[6]: # 🏆 特工榜單
        st.subheader("🏆 全球特工資產排行榜")
        df_list = [{"特工代號": u.get("user", "未知"), "階級身分": u.get("rank", "菜鳥特工"), "總資產 (PTS)": u.get("points", 0), "黑歷史違規": u.get("failed_count", 0)} for u in users if u.get("status") == "active"]
        if df_list: 
            df_sorted = pd.DataFrame(df_list).sort_values(by="總資產 (PTS)", ascending=False)
            st.dataframe(df_sorted, use_container_width=True, hide_index=True)

    with tabs[7]: # 🏪 黑市商店
        st.subheader("🏪 天網黑市高階資產交易端")
        normals = [i for i in shop_items if i.get("type") == "normal"]
        ranks = [i for i in shop_items if i.get("type") == "rank"]
        
        st.markdown("#### 📦 戰術與防禦物資 (購買自動存入背包)")
        cols1 = st.columns(3)
        for idx, item in enumerate(normals):
            with cols1[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"**{item.get('name')}**")
                    st.caption(item.get('desc'))
                    st.write(f"💵 售價: `{item.get('price')} PTS`")
                    if st.button("解鎖此物資", key=f"buy_n_{item.get('id')}", use_container_width=True):
                        if pts >= item.get('price', 0):
                            if u_data:
                                u_data["points"] -= item.get('price', 0)
                                if "inventory" not in u_data: u_data["inventory"] = {}
                                u_data["inventory"][item.get('id')] = u_data["inventory"].get(item.get('id'), 0) + 1
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"購買了物資: {item.get('name')}", current_agent)
                                play_synth_sound("beep")
                                st.success("商品成功購買並空投存入背包！")
                                time.sleep(0.5)
                                st.rerun()
                        else: 
                            st.error("您個人的 PTS 積分餘額不足。")
                        
        st.divider()
        st.markdown("#### 🎖️ 特工階級考核授權書")
        cols2 = st.columns(2)
        for idx, item in enumerate(ranks):
            with cols2[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"**{item.get('name')}**")
                    st.write(f"考核消耗: `{item.get('price')} PTS`")
                    st.caption(f"前置階級要求: 【{item.get('required_rank')}】")
                    allowed = (rank == item.get("required_rank")) or is_admin
                    if st.button("申請解鎖高級身分", key=f"buy_r_{item.get('id')}", disabled=not allowed, use_container_width=True):
                        if pts >= item.get('price', 0):
                            if u_data:
                                u_data["points"] -= item.get('price', 0)
                                u_data["rank"] = item.get("target_rank")
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"晉升身分為 【{item.get('target_rank')}】", current_agent)
                                play_synth_sound("beep")
                                st.success("身分授權驗證更新成功！")
                                time.sleep(0.5)
                                st.rerun()
                        else: 
                            st.error("您目前的 PTS 積分不足。")

    with tabs[8]: # 📡 訊號傳譯器 (整合合成嗶嗶聲播放功能)
        st.subheader("📡 密碼學與訊號傳譯中心")
        st.caption("供前線特工進行攔截信號與密碼編譯。")
        
        cipher_mode = st.radio("選擇訊號處理模式", ["莫斯密碼 (Morse)", "Base64 機密編碼", "Binary 二進制矩陣"], horizontal=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### 🔒 訊號編譯加密 (Encode)")
            input_text = st.text_input("輸入欲編譯的英文/數字明文", placeholder="Skynet Secure Pass 123", key="cipher_encrypt_input")
            if st.button("執行信號封鎖加密", use_container_width=True):
                if input_text:
                    if cipher_mode == "莫斯密碼 (Morse)":
                        res_code = encrypt_morse(input_text)
                    elif cipher_mode == "Base64 機密編碼":
                        res_code = base64.b64encode(input_text.encode('utf-8')).decode('utf-8')
                    else:
                        res_code = ' '.join(format(ord(x), '08b') for x in input_text)
                    
                    play_synth_sound("beep")
                    st.success("🔐 編譯完成，密碼矩陣：")
                    st.code(res_code, language="plaintext")
                else:
                    st.error("請輸入欲加密內容。")
                    
        with col_c2:
            st.markdown("#### 🔓 訊號解碼解密 (Decode)")
            input_cipher = st.text_input("輸入待譯碼的密文信號", placeholder=".-. .- -. -.. --- --", key="cipher_decrypt_input")
            if st.button("執行信號解碼傳譯", use_container_width=True):
                if input_cipher:
                    try:
                        if cipher_mode == "莫斯密碼 (Morse)":
                            res_plain = decrypt_morse(input_cipher)
                        elif cipher_mode == "Base64 機密編碼":
                            res_plain = base64.b64decode(input_cipher.encode('utf-8')).decode('utf-8')
                        else:
                            binary_values = input_cipher.split(' ')
                            ascii_string = ""
                            for bv in binary_values:
                                ascii_string += chr(int(bv, 2))
                            res_plain = ascii_string
                        
                        play_synth_sound("beep")
                        st.success("🔓 傳譯解碼明文：")
                        st.code(res_plain, language="plaintext")
                    except Exception as e:
                        st.error(f"解碼不匹配，無法轉譯: {str(e)}")
                else:
                    st.error("請輸入密文信號。")

    with tabs[9]: # 📢 公共廣播
        st.subheader("📢 戰情公共廣播頻道")
        col_ai1, col_ai2, col_del = st.columns([1,1,2])
        with col_ai1:
            if st.button("🤖 AI 頻道防禦掃描", use_container_width=True):
                chats.append({"sender": "🤖 天網 AI", "text": "[系統日誌] 偵測到廣播信道受到多次黑客震盪，防禦防火牆已重新合攏。"})
                DataManager.save(CHAT_FILE, chats); st.rerun()
        with col_ai2:
            if st.button("📊 AI 全局數據簡報", use_container_width=True):
                chats.append({"sender": "🤖 天網 AI", "text": f"[實時數據] 當前全局活動任務共計 {len(tasks)} 件。"})
                DataManager.save(CHAT_FILE, chats); st.rerun()
        with col_del:
            if is_admin:
                if st.button("🗑 *物理抹除所有廣播紀錄*", type="primary", use_container_width=True):
                    DataManager.save(CHAT_FILE, [])
                    st.rerun()

        st.divider()
        # 僅顯示最新 30 條廣播
        for m in chats[-30:]: 
            st.write(f"**{m.get('sender')}**: {m.get('text')}")
            
        if msg := st.chat_input("發送全局戰情廣播..."):
            chats.append({"sender": current_agent, "text": msg})
            DataManager.save(CHAT_FILE, chats); st.rerun()

    with tabs[10]: # 🔐 私密通訊
        st.subheader("🔐 1 對 1 點對點雙向加密通訊")
        all_agents = [u.get("user") for u in users if u.get("status") == "active" and u.get("user") != current_agent]
        target_p = st.selectbox("請指定加密信道接收方", all_agents)
        if target_p:
            my_privates = [p for p in private_chats if (p.get("sender") == current_agent and p.get("receiver") == target_p) or (p.get("sender") == target_p and p.get("receiver") == current_agent)]
            for pm in my_privates[-20:]: 
                st.write(f"**{pm.get('sender')}**: {pm.get('text')}")
            p_msg = st.chat_input("輸入絕密通訊內容...", key="p_input")
            if p_msg:
                private_chats.append({"sender": current_agent, "receiver": target_p, "text": p_msg, "time": str(datetime.now())})
                DataManager.save(PRIVATE_CHAT_FILE, private_chats); st.rerun()

    with tabs[11]: # 📂 調查線索庫
        st.subheader("📂 天網核心調查線索庫")
        high_ranks = ["天網審判官", "影子特工", "幽靈傳奇"]
        if not is_admin and rank not in high_ranks:
            st.error("🔒 權限拒絕！此核心檔案庫僅限高階權限特工存取。")
        else:
            st.success("🔓 核心探員權限驗證通過。歡迎讀寫與加密歸檔。")
            with st.form("invest_form", clear_on_submit=True):
                title = st.text_input("情報檔案標題")
                content = st.text_area("情報詳細內容")
                if st.form_submit_button("執行加密歸檔") and title and content:
                    invest_data.append({"id": str(int(datetime.now().timestamp())), "title": title, "content": content, "author": current_agent, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    DataManager.save(INVEST_FILE, invest_data)
                    log_activity(f"歸檔了全新核心情報線索: {title}", current_agent)
                    st.success("情報已被加密入庫。")
                    time.sleep(0.5)
                    st.rerun()
            st.divider()
            for inv in invest_data[::-1]: 
                with st.expander(f"🗂️ 檔案：{inv.get('title')} ({inv.get('date')} | 歸檔來源: {inv.get('author')})"):
                    st.write(inv.get('content'))

    with tabs[12]: # 👑 指揮中心
        if not is_admin:
            st.error("🔒 拒絕存取：此頁籤為最高指揮官專用核心節點。")
        else:
            st.subheader("👑 天網最高指揮官控制台")
            
            is_locked = sys_config.get("fake_lock", False)
            col_lk1, col_lk2 = st.columns([3, 1])
            with col_lk1:
                if is_locked: st.error("🔴 當前防禦牆狀態：【緊急假封鎖中】")
                else: st.success("🟢 當前防禦牆狀態：【正常營運中】")
            with col_lk2:
                if is_locked:
                    if st.button("🔓 撤銷全體假封鎖", use_container_width=True):
                        sys_config["fake_lock"] = False
                        DataManager.save(CONFIG_FILE, sys_config)
                        log_activity("指揮官撤銷假封鎖狀態", current_agent)
                        st.rerun()
                else:
                    if st.button("🔒 啟動全防禦假封鎖", type="primary", use_container_width=True):
                        sys_config["fake_lock"] = True
                        DataManager.save(CONFIG_FILE, sys_config)
                        log_activity("指揮官啟動緊急假封鎖協定", current_agent)
                        st.rerun()
            
            st.divider()
            
            # --- ⏳ 新進特工註冊審核中心 ---
            st.markdown("### ⏳ 新進特工註冊審核中心")
            pending_users = [u for u in users if u.get("status") == "pending"]
            
            if pending_users:
                st.info(f"🛰️ 偵測到有 {len(pending_users)} 個新進帳號申請案待處理：")
                for idx, pu in enumerate(pending_users):
                    with st.container(border=True):
                        col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                        with col_u1:
                            st.markdown(f"🕵️‍♂️ **申請特工 ID:** `{pu.get('user')}`")
                            st.caption(f"📅 遞交時間: {pu.get('created_at', '無歷史紀錄')}")
                        with col_u2:
                            if st.button("✅ 批准授權入庫", key=f"approve_{pu.get('user')}_{idx}", use_container_width=True):
                                pu["status"] = "active"
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"最高指揮官批准了特工註冊申請: {pu.get('user')}", current_agent)
                                st.success(f"已核准特工 {pu.get('user')} ！")
                                time.sleep(0.5)
                                st.rerun()
                        with col_u3:
                            if st.button("❌ 拒絕並抹除檔案", key=f"reject_{pu.get('user')}_{idx}", type="primary", use_container_width=True):
                                users = [u for u in users if u.get("user") != pu.get("user")]
                                DataManager.save(USERS_FILE, users)
                                log_activity(f"最高指揮官拒絕並物理抹除了 {pu.get('user')} 的帳號申請案", current_agent)
                                st.warning(f"已粉碎 {pu.get('user')} 的申請檔案。")
                                time.sleep(0.5)
                                st.rerun()
            else:
                st.success("🟢 當前無任何待處理的特工帳號申請。")
            
            st.divider()

            # --- 🛠️ 指揮官自主上架黑市商品機制 ---
            st.markdown("### 🏪 指揮官黑市物資管控系統 (新增商品上架)")
            with st.form("admin_shop_form", clear_on_submit=True):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    new_item_name = st.text_input("📦 全新道具名稱")
                    new_item_price = st.number_input("💰 PTS 售價設定", min_value=1, value=500)
                with col_s2:
                    new_item_desc = st.text_input("📝 道具效果說明")
                    new_item_id = f"custom_item_{int(datetime.now().timestamp())}"
                
                if st.form_submit_button("🔨 執行物品防禦空投上架"):
                    if new_item_name and new_item_desc:
                        shop_items.append({
                            "id": new_item_id,
                            "name": new_item_name,
                            "price": int(new_item_price),
                            "desc": new_item_desc,
                            "type": "normal"
                        })
                        DataManager.save(SHOP_FILE, shop_items)
                        log_activity(f"於黑市上架了新商品: {new_item_name}", current_agent)
                        st.success(f"商品 【{new_item_name}】 已向黑市完成發布！")
                        st.rerun()
                    else:
                        st.error("商品名稱與描述皆為必填！")

            st.divider()
            
            # --- 💰 中央資產與身分干預系統 ---
            st.markdown("### 💰 特工資產與身分中央干預系統")
            active_agent_names = [u.get("user") for u in users if u.get("status") == "active"]
            
            if active_agent_names:
                selected_edit_user = st.selectbox("選擇要操控的特工目標", active_agent_names, key="admin_edit_user_select")
                target_u_data = next((u for u in users if u.get("user") == selected_edit_user), None)
                
                if target_u_data:
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.markdown(f"**當前積分值：** `{target_u_data.get('points', 0)}` PTS")
                        modify_pts = st.number_input("增減積分數量", step=100, value=0, key="modify_pts_input")
                        if st.button("🛠️ 執行積分干預", use_container_width=True):
                            target_u_data["points"] = target_u_data.get("points", 0) + modify_pts
                            DataManager.save(USERS_FILE, users)
                            log_activity(f"中央調整了 {selected_edit_user} 的積分（異動: {modify_pts}）", current_agent)
                            st.rerun()
                            
                    with col_m2:
                        st.markdown(f"**當前階級：** `{target_u_data.get('rank', '菜鳥特工')}`")
                        all_rank_titles = ["菜鳥特工", "資深探員", "王牌特工", "幽靈傳奇", "影子特工", "天網審判官"]
                        try: default_idx = all_rank_titles.index(target_u_data.get('rank', '菜鳥特工'))
                        except ValueError: default_idx = 0
                            
                        new_rank_select = st.selectbox("強制賦予全新特工階級", all_rank_titles, index=default_idx)
                        if st.button("🎖️ 執行階級變更令", use_container_width=True):
                            target_u_data["rank"] = new_rank_select
                            DataManager.save(USERS_FILE, users)
                            log_activity(f"中央變更了 {selected_edit_user} 的正式階級為 {new_rank_select}", current_agent)
                            st.rerun()
                            
                st.markdown("#### 👤 該特工活體檔案核心結構鏡")
                st.json(target_u_data)
            
            st.divider()
            
            # --- 💥 物理除名罪刑系統 ---
            st.markdown("### 💥 終極懲戒除名區")
            if active_agent_names:
                to_del = st.selectbox("選擇要徹底抹除的已活化特工", active_agent_names, key="delete_user_select")
                if st.button("💥 執行最高懲戒：檔案物理抹除", type="primary", use_container_width=True):
                    users = [u for u in users if u.get("user") != to_del]
                    DataManager.save(USERS_FILE, users)
                    log_activity(f"執行了對特工 {to_del} 的核心檔案物理抹除", current_agent)
                    st.rerun()
            
            st.divider()
            st.markdown("#### 📝 全局操作日誌紀錄 (最新 100 筆)")
            st.write(DataManager.load(LOG_FILE))
