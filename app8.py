import random
import time
import os

def clear_screen():
    """ターミナル画面をクリアする（入力内容を次の人に見られないようにするため）"""
    os.system('cls' if os.name == 'nt' else 'clear')

class BorderlandTrainMultiplay:
    def __init__(self, num_human_players=3, total_players=5, num_cars=4):
        self.num_cars = num_cars
        self.players = {}
        
        # プレイヤーの初期化（人間 + 足りない分はNPC）
        for i in range(total_players):
            p_id = f"Player_{i+1}"
            is_human = i < num_human_players
            self.players[p_id] = {
                "car": 0, 
                "is_heart": False, 
                "is_alive": True, 
                "is_human": is_human
            }
        
        # ハート（ターゲット）をランダムに一人決定
        heart_id = random.choice(list(self.players.keys()))
        self.players[heart_id]["is_heart"] = True

    def play_turn(self, turn):
        print(f"\n====================")
        print(f"   TURN {turn} / 5")
        print(f"====================")

        # 1. 全員の移動先を入力（一斉に移動させるために一時保存）
        moves = {}

        for p_id, info in self.players.items():
            if not info["is_alive"]:
                continue

            if info["is_human"]:
                # 人間の入力（他の人に見られないよう画面を隠す案内を入れる）
                clear_screen()
                print(f"--- {p_id} の番です (Enterを押すと開始) ---")
                input()
                if info["is_heart"]:
                    print("🔴 あなたは【ハート】です！")
                
                while True:
                    try:
                        move = int(input(f"{p_id} さん、移動先 (0-{self.num_cars-1}) を選んでください: "))
                        if 0 <= move < self.num_cars:
                            moves[p_id] = move
                            break
                        print("エラー: 存在する車両を選んでください。")
                    except ValueError:
                        print("エラー: 数字を入力してください。")
                clear_screen()
                print("次の人に代わってください...")
                time.sleep(1)
            else:
                # NPCの移動
                moves[p_id] = random.randint(0, self.num_cars - 1)

        # 2. 全員の入力が終わったので、一斉に車両へ移動
        for p_id, target_car in moves.items():
            self.players[p_id]["car"] = target_car

        clear_screen()
        print("全員の移動が完了しました！ 結果を表示します...")
        time.sleep(1)

        # 3. 車両ごとの生存判定
        car_occupants = {i: [] for i in range(self.num_cars)}
        for p_id, info in self.players.items():
            if info["is_alive"]:
                car_occupants[info["car"]].append(p_id)

        for car, occupants in car_occupants.items():
            has_heart = any(self.players[p]["is_heart"] for p in occupants)
            print(f"\n[{car}号車]: {' / '.join(occupants)}")
            
            if has_heart:
                for p in occupants:
                    if not self.players[p]["is_heart"]:
                        print(f" ⚠️  {p} は排除されました。")
                        self.players[p]["is_alive"] = False

    def start(self):
        print("【今際の国のアリス：暴走電車 マルチプレイ】")
        num_h = sum(1 for p in self.players.values() if p["is_human"])
        print(f"参加人数: {num_h}名 / NPC: {len(self.players)-num_h}名")
        input("\nEnterキーでゲーム開始...")

        for t in range(1, 6):
            self.play_turn(t)
            
            # 人間プレイヤーの生存確認
            human_survivors = [p for p, info in self.players.items() if info["is_human"] and info["is_alive"]]
            if not human_survivors:
                # ハートが人間だった場合、生存者がいなければ勝利
                heart_id = [p for p, i in self.players.items() if i["is_heart"]][0]
                if self.players[heart_id]["is_human"]:
                    print("\nGAME CLEAR: ハート（あなた）が全員を排除しました！")
                else:
                    print("\nGAME OVER: 人間プレイヤーは全滅しました。")
                break

            input("\n次のターンへ進む (Enter)...")
        else:
            print("\nGAME CLEAR: 制限時間終了！生き残ったプレイヤーの勝利です。")

if __name__ == "__main__":
    # 人間3人、合計5人で遊ぶ設定
    game = BorderlandTrainMultiplay(num_human_players=3)
    game.start()
