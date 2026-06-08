import streamlit as st
import random
import math
import time

# 設定網頁標題與佈局
st.set_page_config(page_title="Terry's Adventure - AI Edition", layout="centered")

# ==========================================
# 初始化所有遊戲數據 (Session State)
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.game_state = "select"  # select, game, shop
    st.session_state.selected_character = None
    st.session_state.current_level = 1
    st.session_state.max_levels = 1000
    st.session_state.score = 0
    st.session_state.gems = 100
    st.session_state.hp = 100
    st.session_state.max_hp = 100
    st.session_state.clones_count = 0
    st.session_state.atk_buffs_count = 0
    st.session_state.afk_mode = False
    
    # 被動升級
    st.session_state.passive_dmg_lv = 0
    st.session_state.passive_speed_lv = 0
    st.session_state.passive_defense_lv = 0

# 計算過關所需分數 (對應原本 get_score_to_next_level 邏輯)
def get_score_to_next_level(level):
    base = 5
    tier = level // 50
    # 模擬隨機波動
    wave = random.randint(-2, 3)
    return max(3, base + (tier * 4) + wave)

score_to_next_level = get_score_to_next_level(st.session_state.current_level)

# ==========================================
# 遊戲標題與 UI 頂部狀態欄
# ==========================================
st.title("Terry's Adventure ⚡")
st.subheader("1000% Hyper Speed AI Streamlit Edition")

if st.session_state.game_state == "select":
    # ------------------------------------------
    # 角色選擇畫面
    # ------------------------------------------
    st.write("### 👥 請選擇你的英雄角色：")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    
    if col_b1.button("🔥 Blaze (烈焰)", use_container_width=True):
        st.session_state.selected_character = "Blaze"
        st.session_state.game_state = "game"
        st.rerun()
    if col_b2.button("❄️ Frost (寒冰)", use_container_width=True):
        st.session_state.selected_character = "Frost"
        st.session_state.game_state = "game"
        st.rerun()
    if col_b3.button("⚡ Volt (閃電)", use_container_width=True):
        st.session_state.selected_character = "Volt"
        st.session_state.game_state = "game"
        st.rerun()
    if col_b4.button("🍃 Nature (自然)", use_container_width=True):
        st.session_state.selected_character = "Nature"
        st.session_state.game_state = "game"
        st.rerun()

else:
    # ------------------------------------------
    # 核心遊戲與主推關畫面
    # ------------------------------------------
    # 儀表板資料更新
    col1, col2, col3 = st.columns(3)
    col1.metric("STAGE 關卡", f"{st.session_state.current_level} / {st.session_state.max_levels}")
    col2.metric("GEMS 寶石 💎", f"{st.session_state.gems}")
    
    hp_display = "INFINITY (無敵)" if st.session_state.afk_mode else f"{st.session_state.hp}/{st.session_state.max_hp}"
    col3.metric("HP 生命值", hp_display)

    # 功能控制區
    st.markdown("---")
    afk_text = "🟢 關閉 HYPER AFK" if st.session_state.afk_mode else "⚡ 開啟 HYPER AFK (AI 1000% 注入)"
    if st.button(afk_text, use_container_width=True, type="primary" if st.session_state.afk_mode else "secondary"):
        st.session_state.afk_mode = not st.session_state.afk_mode
        if st.session_state.afk_mode:
            st.session_state.hp = 999999999
        else:
            st.session_state.hp = 100
            st.session_state.max_hp = 100
        st.rerun()

    # 動態畫面渲染錨點
    game_canvas = st.empty()
    action_log = st.empty()

    # 執行 AI 自動掛機核心邏輯
    if st.session_state.afk_mode:
        # 模擬原本 60FPS 運作，在一次網頁重新整理中跑 20 幀邏輯，加速網頁反應
        for _ in range(20):
            time.sleep(0.05) # 控制更新頻率防止流暢度雪崩
            
            # 1. 💥 【AI 加速 1000% 注入】：25% 幾率觸發分身海繁衍
            if random.random() < 0.25:
                spawnED_clones = random.randint(8, 15)
                st.session_state.clones_count += spawnED_clones
                st.session_state.atk_buffs_count += spawnED_clones * 12
            
            # 分身鏈式爆發 (15% 幾率分身再分裂)
            if random.random() < 0.15 and st.session_state.clones_count > 0:
                st.session_state.clones_count += int(st.session_state.clones_count * 0.1) + 1
            
            # 2. 怪物生成與斬殺
            spawn_rate = 0.25 # 掛機模式生怪快 5 倍
            if random.random() < spawn_rate:
                # 計算傷害 (包含基礎與分身 Buff 攻擊力)
                damage_deal = 1 + st.session_state.passive_dmg_lv + (st.session_state.atk_buffs_count // 10)
                st.session_state.score += random.randint(1, 2)
                st.session_state.gems += random.randint(1, 2)
                
            # 3. 減緩 Buff 持續時間
            if st.session_state.atk_buffs_count > 0:
                st.session_state.atk_buffs_count = max(0, st.session_state.atk_buffs_count - 5)

            # 4. 檢查過關並自動進入「AI 商店自動購買」
            if st.session_state.score >= score_to_next_level:
                # 商店自動購買邏輯
                if st.session_state.gems >= 4:
                    st.session_state.gems -= 4
                    st.session_state.passive_dmg_lv += 1
                elif st.session_state.gems >= 4:
                    st.session_state.gems -= 4
                    st.session_state.passive_speed_lv += 1
                elif st.session_state.gems >= 5:
                    st.session_state.gems -= 5
                    st.session_state.passive_defense_lv += 1
                
                # 進入下一關
                st.session_state.current_level += 1
                st.session_state.score = 0
                st.session_state.clones_count = int(st.session_state.clones_count * 0.1) # 繼承部分分身
                
            # 更新動態畫布內容
            progress_pct = min(1.0, st.session_state.score / score_to_next_level)
            with game_canvas.container():
                st.write(f"### ⚔️ 英雄屬性：[{st.session_state.selected_character}] 正在瘋狂掛機中...")
                st.progress(progress_pct, text=f"當前關卡擊殺進度: {st.session_state.score} / {score_to_next_level}")
                
                # 分身視覺表現
                visual_icons = "👥 " * min(15, max(1, st.session_state.clones_count // 15))
                st.info(f"**分身海狀態:** {visual_icons} 目前共有 **{st.session_state.clones_count}** 個影子分身在場上")
            
            with action_log.container():
                st.code(f"""
[SYSTEM LOG - SPEED +1000%⚡]
» Terry 本體與分身大軍正在自動移動、釋放 ULT 終極大絕！
» 目前攻擊晶片等級: Lv.{st.session_state.passive_dmg_lv}  | 速度晶片等級: Lv.{st.session_state.passive_speed_lv}
» 分身攻擊增幅加成: +{st.session_state.atk_buffs_count} ATK
                """)
        
        # 幀結束後強制刷新網頁
        st.rerun()
    else:
        # 手動暫停/非掛機狀態下的 UI 顯示
        st.warning("⏸️ 目前 AI 掛機已暫停。請點擊上方按鈕注入 1000% 超速 AI 進行自動戰鬥！")
        if st.button("↩️ 返回重新選擇角色"):
            st.session_state.game_state = "select"
            st.session_state.clones_count = 0
            st.rerun()