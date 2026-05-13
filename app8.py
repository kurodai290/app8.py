import streamlit as st
import random

st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

if 'game_status' not in st.session_state:
    st.session_state.game_status = "START_SCREEN"

def generate_hint(is_gas):
    """難易度を維持するため、70%の確率で正しいヒントを出し、30%で嘘をつく"""
    true_hint = is_gas
    if random.random() > 0.7: # 30%で逆転
        true_hint = not is_gas
    
    if true_hint:
        return random.choice(["【広告】安全第一。非常時に備えよ。", "【掲示】この車両には防犯カメラが設置されています。", "【落書き】死にたくない死にたくない..."])
    else:
        return random.choice(["【広告】高原の爽やかな空気をあなたに。", "【広告】ミントガムで深呼吸。", "【掲示】空調設備点検済み。"])

def start_new_game():
    st.session_state.current_car = 8
    st.session_state.canisters = 5
    st.session_state.gas_cars = random.sample(range(1, 8), 4)
    st.session_state.logs = ["8号車（最後尾）からスタートしました。"]
    # 最初の車両のヒント
    first_car_gas = 7 in st.session_state.gas_cars
    st.session_state.current_hint = generate_hint(first_car_gas)
    st.session_state.game_status = "PLAYING"

if st.session_state.game_status == "START_SCREEN":
    st.title("今際の国のアリス：暴走でんしゃ")
    st.write("全8車両。4つに毒。中和剤は5つ。")
    st.write("車両の「広告」が空気を暗示しているが、それが真実とは限らない...")
    if st.button("げぇむを開始する"):
        start_new_game()
        st.rerun()

elif st.session_state.game_status == "PLAYING":
    st.title(f"現在：{st.session_state.current_car} 号車")
    st.warning(st.session_state.current_hint) # ヒントを表示
    st.info(f"残りの中和剤：{st.session_state.canisters} 個")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("マスクを使う", disabled=(st.session_state.canisters <= 0)):
            st.session_state.canisters -= 1
            st.session_state.current_car -= 1
            car = st.session_state.current_car
            
            # 毒ガス判定 + 5%の不発確率
            if car in st.session_state.gas_cars:
                if random.random() < 0.05: # 5%で失敗
                    st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤が不発...！")
                    st.session_state.game_status = "GAMEOVER"
                else:
                    st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤で耐えた。")
            else:
                st.session_state.logs.insert(0, f"【{car}号車】空気は正常だ。")
            
            # 次の車両のヒント更新
            if car > 1:
                st.session_state.current_hint = generate_hint((car-1) in st.session_state.gas_cars)
            if car == 1 and st.session_state.game_status == "PLAYING":
                st.session_state.game_status = "CLEAR"
            st.rerun()

    with col2:
        if st.button("マスクを使わない"):
            st.session_state.current_car -= 1
            car = st.session_state.current_car
            
            if car in st.session_state.gas_cars:
                st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！死を悟った。")
                st.session_state.game_status = "GAMEOVER"
            else:
                st.session_state.logs.insert(0, f"【{car}号車】空気は正常だ。運が良かったな。")
                if car > 1:
                    st.session_state.current_hint = generate_hint((car-1) in st.session_state.gas_cars)
                if car == 1:
                    st.session_state.game_status = "CLEAR"
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
    st.success("🎉 CLEAR！生き残った。")
    if st.button("新しいげぇむへ"):
        start_new_game()
        st.rerun()
