import pyautogui
import json
import os
import time

def check_odds_pos():
    coords_path = os.path.join(os.path.dirname(__file__), 'target_coords.json')
    if not os.path.exists(coords_path):
        print("座標ファイルがありません")
        return
    
    with open(coords_path, 'r') as f:
        coords = json.load(f)
    
    if 'odds_btn' not in coords:
        print("odds_btn の座標がありません")
        return
    
    x, y = coords['odds_btn']
    print(f"オッズボタンの記憶位置 ({x}, {y}) にマウスを移動します...")
    print("5秒後に移動します。TARGETを最前面にしてください。")
    time.sleep(5)
    
    # ゆっくり移動して場所を教える
    pyautogui.moveTo(x, y, duration=1.5)
    
    # ブルブル震えてアピール
    for _ in range(3):
        pyautogui.moveRel(10, 0, duration=0.1)
        pyautogui.moveRel(-10, 0, duration=0.1)
    
    print("ここを指しています。合っていますか？")

if __name__ == "__main__":
    check_odds_pos()
