import streamlit as st
import random
import time

st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

# --- セッション状態の初期化 ---
if 'game_status' not in st.session_state:
    st.session_state.game_status = "START_SCREEN"

def start_new_game():
    st.session_state.current_car = 8
    st.session_state.canisters = 5
    st.session_state.gas_cars = random.sample(range(1, 8), 4)
    st.session_state.logs = ["8号車からスタート。先頭まで時間がない！"]
    st.session_state.start_time = time.time() # 車両に入った時間
    st.session_state.game_status = "PLAYING"
    update_hint(7)

def update_hint(next_car):
    is_gas = next_car in st.session_state.gas_cars
    # 70%で正しいヒント、30%で嘘
    true_hint = is_gas if random.random() < 0.7 else not is_gas
    if true_hint:
        st.session_state.current_hint = random.choice(["【広告】安全第一。非常時に備えよ。", "【掲示】この車両には防犯カメラが設置されています。", "【落書き】死にたくない..."])
    else:
        st.session_state.current_hint = random.choice(["【広告】高原の爽やかな空気をあなたに。", "【広告】ミントガムで深呼吸。", "【掲示】空調設備点検済み。"])

def move_car(use_mask, time_out=False):
    if use_mask:
        st.session_state.canisters -= 1
    
    st.session_state.current_car -= 1
    car = st.session_state.current_car
    
    msg_prefix = "【時間切れ！】" if time_out else ""
    
    if car in st.session_state.gas_cars:
        if use_mask:
            if random.random() < 0.05: # 5%不発
                st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤が不発...！")
                st.session_state.game_status = "GAMEOVER"
            else:
                st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤で耐えた。")
        else:
            st.session_state.logs.insert(0, f"{msg_prefix}【{car}号車】⚠️ 毒ガス放出！吸い込んでしまった。")
            st.session_state.game_status = "GAMEOVER"
    else:
        st.session_state.logs.insert(0, f"{msg_prefix}【{car}号車】空気は正常だ。")
        if car == 1:
            st.session_state.game_status = "CLEAR"
        else:
            update_hint(car - 1)
    
    st.session_state.start_time = time.time() # タイマーリセット

# --- 画面描画 ---
if st.session_state.game_status == "START_SCREEN":
    st.title("今際の国のアリス：暴走でんしゃ")
    st.write("各車両の滞在制限時間は **15秒**。")
    st.write("時間を過ぎると強制的に次の車両へ移動させられる（マスクなし）。")
    if st.button("げぇむを開始する"):
        start_new_game()
        st.rerun()

elif st.session_state.game_status == "PLAYING":
    st.title(f"現在：{st.session_state.current_car} 号車")
    
    # --- タイマー処理 ---
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 15 - int(elapsed))
    
    if remaining > 0:
        st.error(f"⚠️ 次の車両放出まで：あと {remaining} 秒")
        st.warning(st.session_state.current_hint)
        st.info(f"残りの中和剤：{st.session_state.canisters} 個")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("マスクを使う", disabled=(st.session_state.canisters <= 0)):
                move_car(True)
                st.rerun()
        with col2:
            if st.button("マスクを使わない"):
                move_car(False)
                st.rerun()
        
        # 1秒ごとに自動更新してカウントダウンを見せる
        time.sleep(1)
        st.rerun()
    else:
        # 時間切れ
        move_car(False, time_out=True)
        st.rerun()

    st.write("--- ログ ---")
    for log in st.session_state.logs:
        st.text(log)

elif st.session_state.game_status == "GAMEOVER":
    st.error("💀 GAME OVER")
    if st.button("もう一度挑戦する"):
        start_new_game()
        st.rerun()

elif st.session_state.game_status == "CLEAR":
    st.balloons()
    st.success("🎉 CLEAR！")
    if st.button("新しいげぇむへ"):
        start_new_game()
        st.rerun()
