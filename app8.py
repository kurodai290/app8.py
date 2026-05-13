import random

def runaway_train_game():
    print("【今際の国のアリス：暴走でんしゃ】")
    print("ルール：全8車両のうち4つに毒ガスがあります。")
    print("あなたは中和剤(キャニスター)を5個持っています。")
    print("先頭の1号車まで辿り着き、電車を停止させればクリアです。\n")

    # 車両設定: 1号車〜8号車 (8号車からスタート)
    # 8号車(スタート)を除いた7車両のうち、4つを毒ガス(True)にする
    cars = [False] * 8
    poison_indices = random.sample(range(0, 7), 4) # 1-7号車のどこか
    for i in poison_indices:
        cars[i] = True
    
    canisters = 5
    current_car = 8

    while current_car > 0:
        print(f"--- 現在 {current_car}号車 ---")
        if current_car == 8:
            print("スタート地点です。ここは安全です。")
        
        # 意思決定
        use_mask = input(f"次の車両へ進みます。マスクを使いますか？ (y/n) [残り中和剤: {canisters}]: ").lower()
        
        if use_mask == 'y':
            if canisters > 0:
                canisters -= 1
                protected = True
                print("マスクを装着しました。")
            else:
                print("中和剤がありません！生身で挑みます。")
                protected = False
        else:
            protected = False
            print("マスクを使いませんでした。")

        # 移動
        current_car -= 1
        print(f"{current_car}号車に入りました...")

        # 判定
        if cars[current_car - 1]: # 車両に毒があるか
            print("⚠️ 毒ガスが放出されました！")
            if protected:
                print("中和剤のおかげで助かりました。")
            else:
                print("毒ガスを吸い込みました。GAME OVER.")
                return
        else:
            print("空気は正常です。")
        
        if current_car == 1:
            print("\n🎉 先頭車両に到達！ブレーキを引いて電車を止めました。")
            print("GAME CLEAR!")
            return
        print("-" * 20)

if __name__ == "__main__":
    runaway_train_game()
