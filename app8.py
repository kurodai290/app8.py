import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

# --- セッション状態の初期化 ---
if 'game_status' not in st.session_state:
    st.session_state.game_status = "START_SCREEN" # 状態: START_SCREEN, PLAYING, GAMEOVER, CLEAR

def start_new_game():
    st.session_state.current_car = 8
    st.session_state.canisters = 5
    st.session_state.gas_cars = random.sample(range(1, 8), 4) # 1〜7号車のうち4つ
    st.session_state.logs = ["8号車（最後尾）からスタートしました。"]
    st.session_state.game_status = "PLAYING"

# --- メインロジック ---

# 1. スタート画面
if st.session_state.game_status == "START_SCREEN":
    st.title("今際の国のアリス：暴走でんしゃ")
    st.write("密室の暴走電車。毒ガスを避け、1号車のブレーキを目指せ。")
    if st.button("げぇむを開始する"):
        start_new_game()
        st.rerun()

# 2. プレイ中画面
elif st.session_state.game_status == "PLAYING":
    st.title(f"現在：{st.session_state.current_car} 号車")
    st.info(f"残りの中和剤：{st.session_state.canisters} 個")

    st.write("次の車両へ進みます。マスク（中和剤）を使いますか？")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("マスクを使う", disabled=(st.session_state.canisters <= 0)):
            # 進行処理
            st.session_state.canisters -= 1
            st.session_state.current_car -= 1
            car = st.session_state.current_car
            
            # 毒ガス判定
            if car in st.session_state.gas_cars:
                st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤で耐えた。")
            else:
                st.session_state.logs.insert(0, f"【{car}号車】空気は正常だ。")
            
            # クリア判定（1号車到達）
            if car == 1:
                st.session_state.game_status = "CLEAR"
            st.rerun()

    with col2:
        if st.button("マスクを使わない"):
            # 進行処理
            st.session_state.current_car -= 1
            car = st.session_state.current_car
            
            # 毒ガス判定
            if car in st.session_state.gas_cars:
                st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！")
                st.session_state.game_status = "GAMEOVER"
            else:
                st.session_state.logs.insert(0, f"【{car}号車】空気は正常だ。")
                # 毒なしで1号車到達
                if car == 1:
                    st.session_state.game_status = "CLEAR"
            st.rerun()

    st.write("--- ログ ---")
    for log in st.session_state.logs:
        st.text(log)

# 3. ゲームオーバー画面
elif st.session_state.game_status == "GAMEOVER":
    st.error("💀 げぇむおーばー：毒ガスを吸い込みました。")
    if st.button("もう一度挑戦する"):
        start_new_game()
        st.rerun()

# 4. クリア画面
elif st.session_state.game_status == "CLEAR":
    st.balloons()
    st.success("🎉 げぇむくりあ！1号車のブレーキを停止させました。")
    if st.button("新しいげぇむを始める"):
        start_new_game()
        st.rerun()
