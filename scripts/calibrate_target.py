import pyautogui
import time
import json
import os
import sys
import winsound

def calibrate():
    print("=== TARGET 座標設定 (垂直リスト形式: 1・2行目の学習) ===")
    print("新しい「1行1会場」の画面で、1行目と2行目を覚え直します。")
    print("-" * 40)
    
    save_path = os.path.join(os.path.dirname(__file__), 'target_coords.json')
    positions = {}
    if os.path.exists(save_path):
        try:
            with open(save_path, 'r') as f:
                positions = json.load(f)
        except:
            pass
    
    steps = [
        ('venue_list_1st', '垂直リストの「1行目」の位置'),
        ('venue_list_2nd', '垂直リストの「2行目」の位置')
    ]
    
    for key, label in steps:
        print(f"\n【設定】 {label}")
        print(f"5秒以内にマウスをその場所（会場名のあたり）に置いてください...")
        for i in range(5, 0, -1):
            print(f"{i}...", end=" ", flush=True)
            winsound.Beep(600, 100)
            time.sleep(1.0)
            
        pos = pyautogui.position()
        positions[key] = (pos.x, pos.y)
        print(f"\n記録完了: {pos}")
        winsound.Beep(1200, 500)
        time.sleep(1)

    # Save to file
    with open(save_path, 'w') as f:
        json.dump(positions, f, indent=4)
        
    print("\n" + "="*40)
    print(f"新画面の座標更新が完了しました！")
    print("="*40)

if __name__ == "__main__":
    calibrate()
