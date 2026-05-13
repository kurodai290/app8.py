import streamlit as st
import random
import time

st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

# --- 初期化 ---
if 'game_status' not in st.session_state:
    st.session_state.game_status = "START_SCREEN"

def start_new_game(player_names):
    st.session_state.players = player_names
    st.session_state.turn_idx = 0
    st.session_state.current_car = 8
    st.session_state.canisters = 5 + (len(player_names) - 2) * 2 # 人数に合わせて中和剤を調整
    st.session_state.gas_cars = random.sample(range(1, 8), 4)
    st.session_state.logs = [f"【{len(player_names)}人】での攻略開始。一人の死は全員の死だ。"]
    st.session_state.start_time = time.time()
    st.session_state.game_status = "PLAYING"
    update_hint(7)

def update_hint(next_car):
    is_gas = next_car in st.session_state.gas_cars
    true_hint = is_gas if random.random() < 0.7 else not is_gas
    if true_hint:
        st.session_state.current_hint = random.choice(["【広告】安全第一。非常時に備えよ。", "【掲示】この車両には防犯カメラが設置されています。", "【落書き】次は死ぬ。"])
    else:
        st.session_state.current_hint = random.choice(["【広告】ミントの香りでリフレッシュ。", "【広告】高原の爽やかな空気。", "【掲示】空調点検済み：良好。"])

def move_car(use_mask, time_out=False):
    current_player = st.session_state.players[st.session_state.turn_idx]
    if use_mask:
        st.session_state.canisters -= 1
    
    st.session_state.current_car -= 1
    car = st.session_state.current_car
    
    msg_prefix = "【時間切れ！】" if time_out else ""
    action_msg = "マスクを使用" if use_mask else "生身で突入"
    
    if car in st.session_state.gas_cars:
        if use_mask and random.random() > 0.05: # 95%成功
            st.session_state.logs.insert(0, f"【{car}号車】{current_player}: {action_msg}。毒ガスを耐え抜いた！")
        else:
            death_reason = "不発" if use_mask else "無防備"
            st.session_state.logs.insert(0, f"【{car}号車】{current_player}: {death_reason}。毒ガスにより死亡。")
            st.session_state.game_status = "GAMEOVER"
    else:
        st.session_state.logs.insert(0, f"【{car}号車】{current_player}: {action_msg}。空気は正常。")
        if car == 1:
            st.session_state.game_status = "CLEAR"
        else:
            update_hint(car - 1)
            # 次のプレイヤーへ
            st.session_state.turn_idx = (st.session_state.turn_idx + 1) % len(st.session_state.players)
    
    st.session_state.start_time = time.time()

# --- 画面構成 ---
if st.session_state.game_status == "START_SCREEN":
    st.title("今際の国のアリス：暴走でんしゃ (Multi)")
    num_players = st.slider("プレイヤー人数", 2, 4, 2)
    names = []
    for i in range(num_players):
        names.append(st.text_input(f"プレイヤー {i+1} の名前", f"Player{i+1}"))
    
    if st.button("げぇむを開始する"):
        start_new_game(names)
        st.rerun()

elif st.session_state.game_status == "PLAYING":
    current_player = st.session_state.players[st.session_state.turn_idx]
    st.title(f"{st.session_state.current_car} 号車")
    st.subheader(f"👉 ターン: {current_player}")
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 15 - int(elapsed))
    
    if remaining > 0:
        st.error(f"決断まで：あと {remaining} 秒")
        st.warning(st.session_state.current_hint)
        st.info(f"共有中和剤：{st.session_state.canisters} 個")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{current_player}がマスクを使う", disabled=(st.session_state.canisters <= 0)):
                move_car(True)
                st.rerun()
        with col2:
            if st.button(f"{current_player}は使わない"):
                move_car(False)
                st.rerun()
        
        time.sleep(1)
        st.rerun()
    else:
        move_car(False, time_out=True)
        st.rerun()

    st.write("--- ログ ---")
    for log in st.session_state.logs:
        st.text(log)

elif st.session_state.game_status == "GAMEOVER":
    st.error("💀 GAME OVER（連帯責任）")
    if st.button("リベンジ"):
        st.session_state.game_status = "START_SCREEN"
        st.rerun()

elif st.session_state.game_status == "CLEAR":
    st.balloons()
    st.success("🎉 SURVIVED. 全員が生還しました。")
    if st.button("トップメニューへ"):
        st.session_state.game_status = "START_SCREEN"
        st.rerun()
