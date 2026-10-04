import streamlit as st
import pandas as pd
import datetime
import time
import random
import string
import io
from PIL import Image

# 頁面基本設定
st.set_page_config(page_title="個人萬用實用工具箱", page_icon="🛠️", layout="wide")

# 初始化 Session State (記憶暫存資料)
if "todos" not in st.session_state:
    st.session_state.todos = pd.DataFrame([
        {"完成": False, "任務內容": "完成專案主體架構", "優先級": "高", "截止日期": datetime.date.today()},
        {"完成": True, "任務內容": "測試Streamlit套件", "優先級": "中", "截止日期": datetime.date.today()}
    ])

if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"日期": datetime.date.today(), "類別": "餐飲", "金額": 120, "備註": "午餐便當"},
        {"日期": datetime.date.today(), "類別": "交通", "金額": 50, "備註": "捷運"}
    ])

if "events" not in st.session_state:
    st.session_state.events = [
        {"名稱": "重要簡報 / 期限", "日期": datetime.date.today() + datetime.timedelta(days=7)}
    ]

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = [
        {"名稱": "Google", "網址": "https://www.google.com"},
        {"名稱": "GitHub", "網址": "https://github.com"}
    ]

if "memo" not in st.session_state:
    st.session_state.memo = "# 隨手記草稿\n- 點擊下方區塊直接編輯\n- 支援 Markdown 語法"


# 側邊欄選單
st.sidebar.title("🛠️ 實用工具箱")
choice = st.sidebar.radio(
    "請選擇功能：",
    [
        "1. 📝 待辦事項看板",
        "2. 💰 個人記帳分析",
        "3. 🔤 智能文本工具箱",
        "4. 🔄 圖片與檔案轉換",
        "5. ⏱️ 專注番茄鐘",
        "6. 🔐 密碼生成與安全評估",
        "7. ⏳ 重要日程倒數計時",
        "8. 🔗 個人常用書籤庫",
        "9. 🧮 單位與匯率計算機",
        "10. 📌 隨手記筆記 (Memo)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("系統狀態：本地綠色免聯網版 🟢")

# ==================== 1. 待辦事項看板 ====================
if choice == "1. 📝 待辦事項看板":
    st.header("📝 待辦事項看板")
    st.caption("可以直接點擊表格修改內容、勾選完成，系統會即時更新。")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        edited_df = st.data_editor(
            st.session_state.todos,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "完成": st.column_config.CheckboxColumn("Status", default=False),
                "優先級": st.column_config.SelectboxColumn("Priority", options=["高", "中", "低"], default="中"),
                "截止日期": st.column_config.DateColumn("DueDate")
            }
        )
        st.session_state.todos = edited_df

    with col2:
        st.subheader("📊 完成進度")
        if not edited_df.empty:
            total = len(edited_df)
            done = len(edited_df[edited_df["完成"] == True])
            progress = done / total if total > 0 else 0
            st.progress(progress)
            st.metric(label="達成率", value=f"{int(progress * 100)}%", delta=f"{done}/{total} 完成")
        
        csv_data = edited_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 匯出待辦清單 (CSV)", data=csv_data, file_name="todos.csv", mime="text/csv")

# ==================== 2. 個人記帳分析 ====================
elif choice == "2. 💰 個人記帳分析":
    st.header("💰 個人記帳與預算分析")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("➕ 新增帳目")
        with st.form("expense_form", clear_on_submit=True):
            exp_date = st.date_input("日期", datetime.date.today())
            exp_cat = st.selectbox("類別", ["餐飲", "交通", "娛樂", "購物", "居住", "其他"])
            exp_amount = st.number_input("金額 (TWD)", min_value=1, value=100, step=10)
            exp_note = st.text_input("備註")
            submitted = st.form_submit_state = st.form_submit_button("新增支出")
            
            if submitted:
                new_data = pd.DataFrame([{"日期": exp_date, "類別": exp_cat, "金額": exp_amount, "備註": exp_note}])
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
                st.success("新增成功！")

    with col2:
        st.subheader("📊 統計視覺化")
        if not st.session_state.expenses.empty:
            total_sum = st.session_state.expenses["金額"].sum()
            st.metric("總累計支出", f"${total_sum:,.0f} 元")
            
            # 分類圖表
            cat_chart = st.session_state.expenses.groupby("類別")["金額"].sum()
            st.bar_chart(cat_chart)
            
            st.write("📜 **詳細歷史紀錄**")
            st.dataframe(st.session_state.expenses, use_container_width=True)
        else:
            st.info("目前尚無記帳紀錄。")

# ==================== 3. 智能文本工具箱 ====================
elif choice == "3. 🔤 智能文本工具箱":
    st.header("🔤 智能文本工具箱")
    
    text_input = st.text_area("請輸入或貼上文字：", height=200)
    
    if text_input:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("總字數 (含空格)", len(text_input))
        c2.metric("純字數 (無空格)", len(text_input.replace(" ", "").replace("\n", "")))
        c3.metric("總行數", len(text_input.splitlines()))
        c4.metric("預估閱讀時間", f"{max(1, len(text_input) // 300)} 分鐘")
        
        st.markdown("---")
        st.subheader("🛠️ 文字快速轉換處理")
        col_a, col_b, col_c = st.columns(3)
        
        if col_a.button("移除空白與空行"):
            cleaned = "\n".join([line.strip() for line in text_input.splitlines() if line.strip()])
            st.text_area("處理結果：", cleaned, height=150)
            
        if col_b.button("轉為全大寫 (UPPERCASE)"):
            st.text_area("處理結果：", text_input.upper(), height=150)
            
        if col_c.button("轉為全小寫 (lowercase)"):
            st.text_area("處理結果：", text_input.lower(), height=150)

# ==================== 4. 圖片與檔案轉換 ====================
elif choice == "4. 🔄 圖片與檔案轉換":
    st.header("🔄 萬能圖片格式轉換器")
    st.caption("支援將 JPG / PNG 等圖片一鍵轉換成 PDF 或其它圖檔格式。")
    
    uploaded_files = st.file_uploader("上傳圖片檔案", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
    
    if uploaded_files:
        target_format = st.selectbox("選擇欲轉換的格式", ["PDF", "PNG", "JPEG", "WEBP"])
        
        if st.button("🚀 開始轉換並下載"):
            if target_format == "PDF":
                images = []
                for file in uploaded_files:
                    img = Image.open(file).convert('RGB')
                    images.append(img)
                
                pdf_output = io.BytesIO()
                images[0].save(pdf_output, format="PDF", save_all=True, append_images=images[1:])
                
                st.download_button(
                    label="📥 下載 PDF 檔案",
                    data=pdf_output.getvalue(),
                    file_name="converted_images.pdf",
                    mime="application/pdf"
                )
                st.success("PDF 轉換完成！")
            else:
                for file in uploaded_files:
                    img = Image.open(file)
                    img_output = io.BytesIO()
                    
                    save_fmt = "JPEG" if target_format == "JPEG" else target_format
                    if save_fmt == "JPEG":
                        img = img.convert("RGB")
                        
                    img.save(img_output, format=save_fmt)
                    new_filename = f"{file.name.split('.')[0]}.{target_format.lower()}"
                    
                    st.download_button(
                        label=f"📥 下載 {new_filename}",
                        data=img_output.getvalue(),
                        file_name=new_filename,
                        mime=f"image/{target_format.lower()}"
                    )

# ==================== 5. 專注番茄鐘 ====================
elif choice == "5. ⏱️ 專注番茄鐘":
    st.header("⏱️ 專注番茄鐘")
    
    col1, col2 = st.columns(2)
    work_mins = col1.number_input("專注時間 (分鐘)", min_value=1, max_value=120, value=25)
    break_mins = col2.number_input("休息時間 (分鐘)", min_value=1, max_value=60, value=5)
    
    if st.button("🎬 開始專注倒數"):
        ph = st.empty()
        total_seconds = work_mins * 60
        
        while total_seconds > 0:
            m, s = divmod(total_seconds, 60)
            ph.metric(label="⏳ 剩餘專注時間", value=f"{m:02d}:{s:02d}")
            time.sleep(1)
            total_seconds -= 1
            
        ph.success("🎉 時間到！辛苦了，休息一下吧！")
        st.balloons()

# ==================== 6. 密碼生成與安全評估 ====================
elif choice == "6. 🔐 密碼生成與安全評估":
    st.header("🔐 密碼生成與安全評估器")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎲 強密碼生成")
        length = st.slider("密碼長度", 8, 32, 16)
        use_upper = st.checkbox("包含大寫字母 (A-Z)", value=True)
        use_digits = st.checkbox("包含數字 (0-9)", value=True)
        use_symbols = st.checkbox("包含特殊符號 (!@#$%^&*)", value=True)
        
        chars = string.ascii_lowercase
        if use_upper: chars += string.ascii_uppercase
        if use_digits: chars += string.digits
        if use_symbols: chars += "!@#$%^&*"
        
        if st.button("生成密碼"):
            pwd = "".join(random.choice(chars) for _ in range(length))
            st.code(pwd, language="")
            
    with col2:
        st.subheader("🛡️ 密碼強度檢測")
        check_pwd = st.text_input("輸入密碼進行測試：", type="password")
        if check_pwd:
            score = 0
            if len(check_pwd) >= 12: score += 2
            elif len(check_pwd) >= 8: score += 1
            if any(c.isupper() for c in check_pwd): score += 1
            if any(c.isdigit() for c in check_pwd): score += 1
            if any(c in "!@#$%^&*" for c in check_pwd): score += 1
            
            if score <= 2:
                st.error("強度：弱 ❌ (容易被破解)")
            elif score <= 4:
                st.warning("強度：中等 ⚠️")
            else:
                st.success("強度：強 🛡️ (極難破解)")

# ==================== 7. 重要日程倒數計時 ====================
elif choice == "7. ⏳ 重要日程倒數計時":
    st.header("⏳ 重要日程倒數管理")
    
    with st.expander("➕ 新增重要日程"):
        event_name = st.text_input("日程名稱", "重要考試 / 專案 Deadline")
        event_date = st.date_input("日期", datetime.date.today() + datetime.timedelta(days=10))
        if st.button("新增日程"):
            st.session_state.events.append({"名稱": event_name, "日期": event_date})
            st.success("新增成功！")
            st.rerun()

    st.subheader("📅 日程倒數清單")
    today = datetime.date.today()
    
    for idx, item in enumerate(st.session_state.events):
        diff = (item["日期"] - today).days
        c1, c2, c3 = st.columns([3, 2, 1])
        c1.write(f"**{item['名稱']}** ({item['日期']})")
        
        if diff > 0:
            c2.info(f"⏳ 剩餘 **{diff}** 天")
        elif diff == 0:
            c2.warning("🔥 就是今天！")
        else:
            c2.gray(f"已過期 {abs(diff)} 天")
            
        if c3.button("刪除", key=f"del_ev_{idx}"):
            st.session_state.events.pop(idx)
            st.rerun()

# ==================== 8. 個人常用書籤庫 ====================
elif choice == "8. 🔗 個人常用書籤庫":
    st.header("🔗 個人常用快捷書籤庫")
    
    with st.expander("➕ 新增常用書籤"):
        b_name = st.text_input("網站名稱")
        b_url = st.text_input("網址 (包含 http:// 或 https://)")
        if st.button("儲存書籤"):
            if b_name and b_url:
                st.session_state.bookmarks.append({"名稱": b_name, "網址": b_url})
                st.success("書籤已儲存！")
                st.rerun()
                
    st.subheader("📌 快捷捷徑")
    cols = st.columns(3)
    for idx, bm in enumerate(st.session_state.bookmarks):
        with cols[idx % 3]:
            st.markdown(f"### [{bm['名稱']}]({bm['網址']})")
            st.caption(bm['網址'])
            if st.button("🗑️ 刪除", key=f"del_bm_{idx}"):
                st.session_state.bookmarks.pop(idx)
                st.rerun()

# ==================== 9. 單位與匯率計算機 ====================
elif choice == "9. 🧮 單位與匯率計算機":
    st.header("🧮 智能單位與匯率計算機")
    
    tab1, tab2 = st.tabs(["💱 常用匯率估算 (以 TWD 為基準)", "📏 長度與重量換算"])
    
    with tab1:
        twd = st.number_input("輸入新台幣金額 (TWD)", min_value=1, value=1000)
        c1, c2, c3 = st.columns(3)
        # 以常見參考匯率計算
        c1.metric("美金 (USD)", f"${twd * 0.031:.2f}")
        c2.metric("日圓 (JPY)", f"¥{twd * 4.65:.1f}")
        c3.metric("韓元 (KRW)", f"₩{twd * 42.5:.1f}")
        st.caption("註：此匯率為參考推估值，實際交易以銀行牌告為準。")

    with tab2:
        val = st.number_input("輸入數值", value=100.0)
        u_type = st.radio("換算類型", ["公分 (cm) ↔ 吋 (inch)", "公斤 (kg) ↔ 磅 (lb)"])
        
        if "公分" in u_type:
            st.write(f"👉 **{val} 公分** = **{val / 2.54:.2f} 吋**")
            st.write(f"👉 **{val} 吋** = **{val * 2.54:.2f} 公分**")
        else:
            st.write(f"👉 **{val} 公斤** = **{val * 2.20462:.2f} 磅**")
            st.write(f"👉 **{val} 磅** = **{val / 2.20462:.2f} 公斤**")

# ==================== 10. 隨手記筆記 (Memo) ====================
elif choice == "10. 📌 隨手記筆記 (Memo)":
    st.header("📌 隨手記筆記 (Markdown Memo)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✏️ 編輯區")
        memo_content = st.text_area("輸入內容：", value=st.session_state.memo, height=350)
        st.session_state.memo = memo_content
        
        st.download_button(
            label="📥 下載筆記 (.md)",
            data=memo_content.encode("utf-8"),
            file_name="memo.md",
            mime="text/markdown"
        )
        
    with col2:
        st.subheader("👁️ 即時預覽")
        st.markdown(st.session_state.memo)
