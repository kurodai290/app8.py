import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="剣道学科試験クイズ", page_icon="⚔️")

# 問題データ
questions = [
    {"id": 1, "q": "全日本剣道連盟制定の「剣道の理念」を記せ。", "a": "剣道は人間形成の道である。", "g": ""},
    {"id": 2, "q": "「剣道修錬の心構え」の空欄を埋めなさい。\n剣道を正しく学び、心身を練磨して旺盛なる（ A ）を養い、剣道の特性を通じて（ B ）を尊び、（ C ）を重んじ、（ D ）を尽くして常に自己の修養に努め、以って、国家社会を愛して広く人類の（ E ）に寄与せんとするものである。", "a": "A:気力、B:礼節、C:信義、D:誠、E:平和繁栄", "g": "礼節・相手・気力・信義・平和繁栄・誠実・克己・忠誠"},
    {"id": 3, "q": "「中段の構え」の空欄を埋めなさい。\n相手を（ A ）にも、自分を（ B ）にも、相手の（ C ）に応ずるにも都合のよい、いわゆる（ D ）の構えで、もっとも（ E ）な構えである。", "a": "A:攻める、B:守る、C:変化、D:攻防自在、E:正しい", "g": "自然・変化・守る・正しい・攻める・勝つ・攻防自在"},
    {"id": 4, "q": "「切り返しの意義」の空欄を埋めなさい。\n切り返しは、（ A ）の動きを柔らかく、（ B ）の動きを巧妙に、進退の動作を早くし、（ C ）を正確に知ることができるとともに、（ D ）を養い、（ E ）の技を修練するものである。", "a": "A:身体手足、B:手の内、C:間合、D:体力気力、E:勝つための", "g": "間合・手の内・剣体一致の一体・体力気力・身体手足・勝つための"},
    {"id": 5, "q": "「気剣体一致」の空欄を埋めなさい。\n気とは、心の（ A ）を言い、剣とは、剣の（ B ）を言い、体とは、身体の（ C ）をいう。この三つが一瞬の間に、正しい状態で、一致して活動することが（ D ）の根本である。", "a": "A:活動状態、B:運用状態、C:行動状態、D:有効打突", "g": "有効打突・運用状態・行動状態・活動状態・試合・心気力の一致"}
]

st.title("⚔️ 剣道学科試験クイズ")

# セッション状態（現在の問題を保持）
if 'current_q' not in st.session_state:
    st.session_state.current_q = random.choice(questions)
    st.session_state.show_answer = False

def next_question():
    st.session_state.current_q = random.choice(questions)
    st.session_state.show_answer = False

# 問題表示
q = st.session_state.current_q
st.subheader(f"問題 {q['id']}")
st.write(q['q'])

if q['g']:
    st.info(f"**語群：** {q['g']}")

# 操作ボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("正解を表示"):
        st.session_state.show_answer = True
with col2:
    st.button("次の問題へ", on_click=next_question)

# 回答表示
if st.session_state.show_answer:
    st.success(f"**【正解】**\n\n{q['a']}")

st.divider()
st.caption("画像を元に作成したランダム出題システムです。")
