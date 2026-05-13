import streamlit as st
import random
import time

st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

# --- 初期化 ---
if 'game_status' not in st.session_state:
    st.session_state.game_status = "START_SCREEN"

def start_new_game(player_names):
    # 各プレイヤーの状態管理（名前、生存、マスク使用回数）
    st.session_state.players = [
        {"name": n, "alive": True, "mask_used": 0} for n in player_names
    ]
    st.session_state.turn_idx = 0
    st.session_state.current_car = 8
    st.session_state.canisters = 5 + (len(player_names) - 2) * 2
    st.session_state.gas_cars = random.sample(range(1, 8), 4)
    st.session_state.logs = [f"【{len(player_names)}人】攻略開始。"]
    st.session_state.start_time = time.time()
    st.session_state.game_status = "PLAYING"
    update_hint(7)

def update_hint(next_car):
    is_gas = next_car in st.session_state.gas_cars
    true_hint = is_gas if random.random() < 0.7 else not is_gas
    if true_hint:
        st.session_state.current_hint = random.choice(["【広告】安全第一。非常時に備えよ。", "【掲示】監視カメラ作動中。", "【落書き】次は死ぬ。"])
    else:
        st.session_state.current_hint = random.choice(["【広告】ミントの香りでリフレッシュ。", "【広告】高原の爽やかな空気。", "【掲示】空調良好。"])

def next_turn():
    original_idx = st.session_state.turn_idx
    while True:
        st.session_state.turn_idx = (st.session_state.turn_idx + 1) % len(st.session_state.players)
        if st.session_state.players[st.session_state.turn_idx]["alive"]:
            break
        if st.session_state.turn_idx == original_idx:
            break
    st.session_state.start_time = time.time()

def move_car(use_mask, time_out=False):
    p_idx = st.session_state.turn_idx
    current_p = st.session_state.players[p_idx]
    
    if use_mask:
        st.session_state.canisters -= 1
        st.session_state.players[p_idx]["mask_used"] += 1
    
    st.session_state.current_car -= 1
    car = st.session_state.current_car
    
    if car in st.session_state.gas_cars:
        if use_mask and random.random() > 0.05:
            st.session_state.logs.insert(0, f"【{car}号車】{current_p['name']}: マスクで耐えた。")
        else:
            st.session_state.players[p_idx]["alive"] = False
            st.session_state.logs.insert(0, f"【{car}号車】💀 {current_p['name']} が死亡。")
    else:
        st.session_state.logs.insert(0, f"【{car}号車】{current_p['name']}: 安全だった。")

    alives = [p for p in st.session_state.players if p["alive"]]
    if not alives:
        st.session_state.game_status = "GAMEOVER"
    elif car == 1:
        st.session_state.game_status = "CLEAR"
    else:
        update_hint(car - 1)
        next_turn()

# --- 画面構成 ---
if st.session_state.game_status == "START_SCREEN":
    st.title("今際の国のアリス：暴走でんしゃ")
    num_players = st.slider("プレイヤー人数", 1, 4, 2)
    names = [st.text_input(f"Player {i+1}", f"Player{i+1}") for i in range(num_players)]
    if st.button("げぇむを開始する"):
        start_new_game(names)
        st.rerun()

elif st.session_state.game_status in ["PLAYING", "GAMEOVER", "CLEAR"]:
    # --- スコアボード (サイドバー) ---
    st.sidebar.title("📋 スコアボード")
    for p in st.session_state.players:
        if p["alive"]:
            st.sidebar.write(f"🟢 **{p['name']}**")
            st.sidebar.caption(f"　マスク使用: {p['mask_used']}回")
        else:
            st.sidebar.write(f"🔴 ~~{p['name']} (死亡)~~")
            st.sidebar.caption(f"　最終記録: マスク {p['mask_used']}回")
    st.sidebar.write("---")
    st.sidebar.write(f"🔋 共有中和剤残り: {st.session_state.canisters}")

    if st.session_state.game_status == "PLAYING":
        p_idx = st.session_state.turn_idx
        current_p = st.session_state.players[p_idx]
        
        st.title(f"{st.session_state.current_car} 号車")
        st.subheader(f"👉 ターン: {current_p['name']}")
        
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 15 - int(elapsed))
        
        if remaining > 0:
            st.error(f"決断まで：あと {remaining} 秒")
            st.warning(st.session_state.current_hint)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("マスクを使う", disabled=(st.session_state.canisters <= 0)):
                    move_car(True)
                    st.rerun()
            with col2:
                if st.button("マスクを使わない"):
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
        st.error("💀 全員死亡しました。")
        if st.button("最初からリトライ"):
            st.session_state.game_status = "START_SCREEN"
            st.rerun()

    elif st.session_state.game_status == "CLEAR":
        st.balloons()
        winners = ", ".join([p["name"] for p in st.session_state.players if p["alive"]])
        st.success(f"🎉 CLEAR！ 生還者: {winners}")
        if st.button("トップメニューへ"):
            st.session_state.game_status = "START_SCREEN"
            st.rerun()
