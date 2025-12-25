import pyautogui
import time
import json
import os
import sys

def test_coordinates():
    # 座標ファイルの読み込み
    coords_path = os.path.join(os.path.dirname(__file__), 'target_coords.json')
    if not os.path.exists(coords_path):
        print(f"Error: Coordinates file not found at {coords_path}")
        return

    with open(coords_path, 'r') as f:
        coords = json.load(f)

    print("=== TARGET 座標テスト開始 ===")
    print("TARGETを起動し、最大化した状態で前面に出しておいてください。")
    print("5秒後にテストを開始します...")
    time.sleep(5)

    for name, pos in coords.items():
        x, y = pos
        print(f"\n[{name}] に移動中: ({x}, {y})")
        print("マウスを動かさないでください...")
        
        # マウスをスムーズに移動
        pyautogui.moveTo(x, y, duration=1.0)
        
        # 確認のために2秒間停止
        time.sleep(2)
        
        # 軽く揺らして「ここだよ」とアピール
        for i in range(3):
            pyautogui.moveRel(10, 0, duration=0.1)
            pyautogui.moveRel(-10, 0, duration=0.1)
        
        print(f"-> {name} の位置を確認してください。")
        time.sleep(1)

    print("\n=== テスト完了 ===")
    print("全ての座標を確認しました。ズレているものがあれば教えてください。")

if __name__ == "__main__":
    try:
        test_coordinates()
    except KeyboardInterrupt:
        print("\n中断されました。")
