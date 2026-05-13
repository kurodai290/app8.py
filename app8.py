import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="今際の国のアリス：暴走でんしゃ", layout="centered")

# --- セッション状態の完全リセット関数 ---
def reset_game():
    st.session_state.current_car = 8
    st.session_state.canisters = 5
    st.session_state.game_over = False
    st.session_state.clear = False
    # 毒ガスの配置（1〜7号車のうち4つ）
    st.session_state.gas_cars = random.sample(range(1, 8), 4)
    st.session_state.logs = ["8号車からスタートしました。"]
    st.session_state.started = True

# --- 初回起動時の処理 ---
if 'started' not in st.session_state:
    st.title("今際の国のアリス：暴走でんしゃ")
    st.write("密室の暴走電車。毒ガスを避け、先頭車両のブレーキを目指せ。")
    if st.button("げぇむを開始する"):
        reset_game()
        st.rerun()
    st.stop() # 開始ボタンを押すまで下のコードを実行させない

# --- ゲーム進行関数 ---
def move_next(use_mask):
    if use_mask:
        st.session_state.canisters -= 1
    
    st.session_state.current_car -= 1
    car = st.session_state.current_car

    if car in st.session_state.gas_cars:
        if use_mask:
            st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！中和剤で耐えた。")
        else:
            st.session_state.logs.insert(0, f"【{car}号車】⚠️ 毒ガス放出！GAME OVER")
            st.session_state.game_over = True
    else:
        st.session_state.logs.insert(0, f"【{car}号車】空気は正常だ。")

    # 1号車に到達し、かつ毒ガスで死んでいない場合のみクリア
    if car == 1 and not st.session_state.game_over:
        st.session_state.clear = True

# --- 画面表示 ---
st.title("暴走でんしゃ")

if st.session_state.game_over:
    st.error("💀 げぇむおーばー：毒ガスを吸い込みました。")
    if st.button("もう一度挑戦する"):
        reset_game()
        st.rerun()

elif st.session_state.clear:
    st.balloons()
    st.success("🎉 げぇむくりあ！電車を停止させました。")
    if st.button("新しくげぇむを始める"):
        reset_game()
        st.rerun()

else:
    # プレイ中の表示
    st.subheader(f"現在：{st.session_state.current_car} 号車")
    st.metric(label="残り中和剤", value=f"{st.session_state.canisters} 個")
    
    st.write("次の車両へ移動しますか？")
    col1, col2 = st.columns(2)
    with col1:
        btn_mask = st.button(f"マスクを使う", disabled=(st.session_state.canisters <= 0))
        if btn_mask:
            move_next(True)
            st.rerun()
    with col2:
        if st.button("マスクを使わない"):
            move_next(False)
            st.rerun()

# ログ表示
st.write("---")
for log in st.session_state.logs:
    st.text(log)
