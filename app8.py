import streamlit as st
import random

# タイトルと説明
st.title("今際の国のアリス：暴走でんしゃ")
st.write("全8車両のうち4つに毒ガスがあります。先頭車両を目指せ。")

# ゲームの状態管理
if 'current_car' not in st.session_state:
    st.session_state.current_car = 8
    st.session_state.canisters = 5
    st.session_state.game_over = False
    st.session_state.clear = False
    # 毒ガスの配置（1〜7号車のうち4つ）
    gas_cars = random.sample(range(1, 8), 4)
    st.session_state.gas_cars = gas_cars
    st.session_state.logs = []

def play_turn(use_mask):
    if st.session_state.game_over or st.session_state.clear:
        return

    if use_mask:
        st.session_state.canisters -= 1
    
    st.session_state.current_car -= 1
    car = st.session_state.current_car

    if car in st.session_state.gas_cars:
        if use_mask:
            st.session_state.logs.append(f"{car}号車：毒ガス放出！マスクで防いだ。")
        else:
            st.session_state.logs.append(f"{car}号車：毒ガス放出！GAME OVER")
            st.session_state.game_over = True
    else:
        st.session_state.logs.append(f"{car}号車：空気は正常。")

    if car == 1 and not st.session_state.game_over:
        st.session_state.clear = True

# 画面表示
st.subheader(f"現在：{st.session_state.current_car} 号車")
st.info(f"残りの中和剤：{st.session_state.canisters} 個")

if not st.session_state.game_over and not st.session_state.clear:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("マスクを使う", disabled=st.session_state.canisters <= 0):
            play_turn(True)
            st.rerun()
    with col2:
        if st.button("マスクを使わない"):
            play_turn(False)
            st.rerun()
elif st.session_state.game_over:
    st.error("💀 げぇむおーばー")
    if st.button("リトライ"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
elif st.session_state.clear:
    st.balloons()
    st.success("🎉 げぇむくりあ！")
    if st.button("もう一度遊ぶ"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# 履歴表示
for log in reversed(st.session_state.logs):
    st.text(log)
