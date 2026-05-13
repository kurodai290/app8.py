<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>今際の国のアリス：暴走でんしゃ</title>
    <style>
        body { background: #111; color: #eee; font-family: sans-serif; text-align: center; padding: 20px; }
        #game-box { max-width: 500px; margin: 0 auto; border: 2px solid #555; padding: 20px; border-radius: 10px; background: #222; }
        button { padding: 10px 20px; margin: 10px; font-size: 16px; cursor: pointer; border-radius: 5px; border: none; }
        .btn-yes { background: #d9534f; color: white; }
        .btn-no { background: #5bc0de; color: white; }
        #log { margin-top: 20px; text-align: left; height: 150px; overflow-y: auto; border-top: 1px solid #444; padding-top: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div id="game-box">
        <h1>暴走でんしゃ</h1>
        <p id="status">現在: 8号車</p>
        <p id="info">残りのキャニスター: 5個</p>
        <div id="controls">
            <p>次の車両でマスクを使いますか？</p>
            <button class="btn-yes" onclick="play(true)">使う</button>
            <button class="btn-no" onclick="play(false)">使わない</button>
        </div>
        <div id="log"></div>
    </div>

    <script>
        let currentCar = 8;
        let canisters = 5;
        // 1〜7号車のうち4つを毒ガス(1)に設定
        let cars = [0,0,0,0,0,0,0];
        let gasIndexes = [0,1,2,3,4,5,6].sort(() => Math.random() - 0.5).slice(0, 4);
        gasIndexes.forEach(i => cars[i] = 1);

        function log(msg) {
            const logBox = document.getElementById('log');
            logBox.innerHTML = msg + "<br>" + logBox.innerHTML;
        }

        function play(useMask) {
            if (useMask && canisters <= 0) {
                log("キャニスターがありません！生身で挑みます。");
                useMask = false;
            }

            if (useMask) canisters--;
            currentCar--;

            document.getElementById('status').innerText = `現在: ${currentCar}号車`;
            document.getElementById('info').innerText = `残りのキャニスター: ${canisters}個`;

            if (cars[currentCar - 1] === 1) {
                log(`⚠️ ${currentCar}号車：毒ガス放出！`);
                if (useMask) {
                    log("中和剤のおかげで助かった...");
                } else {
                    log("<strong>GAME OVER... 毒ガスを吸い込みました。</strong>");
                    document.getElementById('controls').innerHTML = '<button onclick="location.reload()">再挑戦</button>';
                    return;
                }
            } else {
                log(`${currentCar}号車：空気は正常。`);
            }

            if (currentCar === 1) {
                log("<strong>🎉 CLEAR! 先頭車両でブレーキを引きました！</strong>");
                document.getElementById('controls').innerHTML = '<button onclick="location.reload()">もう一度遊ぶ</button>';
            }
        }
    </script>
</body>
</html>
