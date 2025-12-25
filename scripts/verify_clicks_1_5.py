import pyautogui
import time
import json
import os

def verify_clicks():
    # 座標ファイルの読み込み
    coords_path = os.path.join(os.path.dirname(__file__), 'target_coords.json')
    if not os.path.exists(coords_path):
        print(f"Error: Coordinates file not found at {coords_path}")
        return

    with open(coords_path, 'r') as f:
        coords = json.load(f)

    print("=== TARGET 動作テスト (手順1～5) ===")
    print("TARGETを起動し、最初の画面（会場一覧）を出しておいてください。")
    print("5秒後に実際のクリックを開始します...")
    time.sleep(5)

    try:
        # 1. 会場リストの1行目をダブルクリック
        if 'venue_list_1st' in coords:
            x, y = coords['venue_list_1st']
            print(f"1. 会場を開いています... ({x}, {y})")
            pyautogui.doubleClick(x, y)
            time.sleep(5) # 画面遷移待ち
        
        # 2. レースリストの1行目をダブルクリック
        if 'race_list_1st' in coords:
            x, y = coords['race_list_1st']
            print(f"2. レースを開いています... ({x}, {y})")
            pyautogui.doubleClick(x, y)
            time.sleep(3) # 画面遷移待ち

        # 3. オッズボタンをクリック
        if 'odds_btn' in coords:
            x, y = coords['odds_btn']
            print(f"3. オッズ画面を表示中... ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(3)

        # 4. 単複時系タグをクリック
        if 'jikei_tab' in coords:
            x, y = coords['jikei_tab']
            print(f"4. 単複時系タブに切り替え中... ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(2)

        # 5. JVオッズ取得ボタンをクリック
        if 'jv_get_btn' in coords:
            x, y = coords['jv_get_btn']
            print(f"5. JVオッズ取得ボタンをクリックしました。 ({x}, {y})")
            pyautogui.click(x, y)
            # ここでDLが始まるはず（音などが鳴るか確認）
            time.sleep(2)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    print("\n=== テスト完了 ===")
    print("正しく遷移しましたか？ JVオッズ取得まで進んでいれば成功です。")

if __name__ == "__main__":
    verify_clicks()
