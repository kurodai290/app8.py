<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>剣道学科試験クイズ</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 20px auto; padding: 0 10px; line-height: 1.6; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .question-text { font-weight: bold; font-size: 1.1em; margin-bottom: 15px; white-space: pre-wrap; }
        .word-group { background: #eef; padding: 10px; border-radius: 4px; font-size: 0.9em; margin-bottom: 15px; }
        .answer-area { display: none; background: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-top: 15px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; }
        button:hover { background: #0056b3; }
        .controls { margin-top: 20px; display: flex; gap: 10px; }
    </style>
</head>
<body>

    <h1>剣道学科試験クイズ</h1>
    <div id="quiz-container" class="card">
        <div id="question" class="question-text">読み込み中...</div>
        <div id="word-group" class="word-group"></div>
        <button onclick="showAnswer()">正解を表示</button>
        <div id="answer" class="answer-area"></div>
        
        <div class="controls">
            <button onclick="nextQuestion()" style="background:#28a745;">次の問題へ（ランダム）</button>
        </div>
    </div>

    <script>
        const questions = [
            { id: 1, q: "全日本剣道連盟制定の「剣道の理念」を記せ。", a: "剣道は人間形成の道である。", g: "" },
            { id: 2, q: "「剣道修錬の心構え」の空欄を埋めなさい。\n剣道を正しく学び、心身を練磨して旺盛なる（ A ）を養い、剣道の特性を通じて（ B ）を尊び、（ C ）を重んじ、（ D ）を尽くして常に自己の修養に努め、以って、国家社会を愛して広く人類の（ E ）に寄与せんとするものである。", a: "A:気力、B:礼節、C:信義、D:誠、E:平和繁栄", g: "礼節・相手・気力・信義・平和繁栄・誠実・克己・忠誠" },
            { id: 3, q: "「中段の構え」の空欄を埋めなさい。\n相手を（ A ）にも、自分を（ B ）にも、相手の（ C ）に応ずるにも都合のよい、いわゆる（ D ）の構えで、もっとも（ E ）な構えである。", a: "A:攻める、B:守る、C:変化、D:攻防自在、E:正しい", g: "自然・変化・守る・正しい・攻める・勝つ・攻防自在" },
            { id: 4, q: "「切り返しの意義」の空欄を埋めなさい。\n切り返しは、（ A ）の動きを柔らかく、（ B ）の動きを巧妙に、進退の動作を早くし、（ C ）を正確に知ることができるとともに、（ D ）を養い、（ E ）の技を修練するものである。", a: "A:身体手足、B:手の内、C:間合、D:体力気力、E:勝つための", g: "間合・手の内・剣体一致の一体・体力気力・身体手足・勝つための" },
            { id: 5, q: "「気剣体一致」の空欄を埋めなさい。\n気とは、心の（ A ）を言い、剣とは、剣の（ B ）を言い、体とは、身体の（ C ）をいう。この三つが一瞬の間に、正しい状態で、一致して活動することが（ D ）の根本である。", a: "A:活動状態、B:運用状態、C:行動状態、D:有効打突", g: "有効打突・運用状態・行動状態・活動状態・試合・心気力の一致" }
        ];

        let currentQ = {};

        function nextQuestion() {
            const randomIndex = Math.floor(Math.random() * questions.length);
            currentQ = questions[randomIndex];
            document.getElementById('question').innerText = `【問題 ${currentQ.id}】\n${currentQ.q}`;
            document.getElementById('answer').style.display = 'none';
            document.getElementById('answer').innerText = `【正解】\n${currentQ.a}`;
            
            const wg = document.getElementById('word-group');
            if(currentQ.g) {
                wg.innerText = `語群：${currentQ.g}`;
                wg.style.display = 'block';
            } else {
                wg.style.display = 'none';
            }
        }

        function showAnswer() {
            document.getElementById('answer').style.display = 'block';
        }

        // 初回起動
        nextQuestion();
    </script>
</body>
</html>
