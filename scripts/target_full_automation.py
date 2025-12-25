import pyautogui
import time
import json
import os
import logging
import sys
from datetime import datetime
import win32api
import win32con
from PIL import ImageChops

# ロギング設定
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/target_auto_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# PyAutoGUI設定
pyautogui.FAILSAFE = True  # マウスを左上に持っていくと強制終了
pyautogui.PAUSE = 0.1      # コマンド間の待機時間を大幅短縮（0.5 -> 0.1）

def check_stop_signal():
    """Escキーが押されているかチェック"""
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) != 0:
        logger.warning("!!! Escキーによる緊急停止を検知しました !!!")
        sys.exit(0)

def get_list_screenshot(region):
    """リスト領域のスクリーンショットを取得"""
    return pyautogui.screenshot(region=region)

def run_automation():
    # 座標ファイルの読み込み
    coords_path = os.path.join(os.path.dirname(__file__), 'target_coords.json')
    if not os.path.exists(coords_path):
        logger.error(f"座標ファイルが見つかりません: {coords_path}")
        return

    with open(coords_path, 'r') as f:
        coords = json.load(f)

    # 必須座標の確認
    required = ['odds_btn', 'jikei_tab', 'jv_get_btn', 'csv_menu_item', 
                'close_odds_x', 'next_race_btn', 'close_race_x', 'venue_list_1st', 'race_list_1st']
    for req in required:
        if req not in coords:
            logger.error(f"座標が不足しています: {req}")
            return

    # 設定
    num_venues = 500  # 実質無限（自動停止に任せる）
    num_races = 12    # 全12レース取得
    
    # 画面変化検知用の領域 (venue_list_1stの周辺 400x400程度を監視)
    v_x, v_y = coords['venue_list_1st']
    detect_region = (max(0, v_x - 50), max(0, v_y - 50), 400, 400)

    logger.info("=== TARGET 全自動取得プログラム (高速機敏版) ===")
    logger.info("垂直リストの1行目を選択した状態で待機してください。")
    logger.info("【停止方法】 Escキーを長押し または マウスを左上スミへ")
    logger.info("5秒後に開始します...")
    time.sleep(5)

    try:
        for v_idx in range(num_venues):
            check_stop_signal() # 緊急停止チェック
            logger.info(f"========== 開催 {v_idx + 1} 処理中 ==========")
            
            # 1. 現在のリスト状態を撮影
            pre_img = get_list_screenshot(detect_region)

            # 手順1: 会場を開く
            pyautogui.press('enter')
            time.sleep(1.5)  # 3s -> 1.5s
            check_stop_signal()

            # 手順2: 1Rを選択
            r_x, r_y = coords['race_list_1st']
            pyautogui.doubleClick(r_x, r_y)
            time.sleep(1.5)  # 3s -> 1.5s

            # 【レースループ】
            for r_idx in range(num_races):
                check_stop_signal()
                logger.info(f"  --- レース {r_idx + 1} / {num_races} ---")
                
                # 手順3: オッズボタン
                pyautogui.click(coords['odds_btn'])
                time.sleep(0.8) # 2s -> 0.8s
                
                # 手順4: 単複時系タブ
                pyautogui.click(coords['jikei_tab'])
                time.sleep(0.4) # 1s -> 0.4s
                
                # 手順5: JVオッズ取得
                pyautogui.click(coords['jv_get_btn'])
                time.sleep(1.2) # 2s -> 1.2s

                # 手順6-7: メニュー
                pyautogui.hotkey('alt', 'f')
                time.sleep(0.3) # 0.5s -> 0.3s
                pyautogui.press('o')
                time.sleep(0.5) # 1s -> 0.5s
                
                # 手順8-9: CSV保存
                pyautogui.click(coords['csv_menu_item'])
                time.sleep(0.2) # 0.5s -> 0.2s
                pyautogui.press('enter')
                time.sleep(0.8) # 2s -> 0.8s

                # 手順10: オッズ画面を閉じる
                pyautogui.click(coords['close_odds_x'])
                time.sleep(0.3) # 1s -> 0.3s

                # 手順11: 次のレースへ
                if r_idx < num_races - 1:
                    pyautogui.click(coords['next_race_btn'])
                    time.sleep(0.8) # 2s -> 0.8s

            # 手順13 & 14: 一覧へ戻る
            pyautogui.click(coords['close_race_x'])
            time.sleep(1.0) # 2s -> 1.0s
            pyautogui.click(coords['close_race_x'])
            time.sleep(1.5) # 3s -> 1.5s

            # 次の開催へ移動
            logger.info("次の開催へ移動...")
            pyautogui.press('down')
            time.sleep(0.8) # 1.5s -> 0.8s
            
            # 2. 移動後のリスト状態を撮影して比較
            post_img = get_list_screenshot(detect_region)
            
            # 画像の差分があるかチェック
            diff = ImageChops.difference(pre_img, post_img)
            if not diff.getbbox():
                logger.info("!!! リストの末尾に達しました。自動停止します !!!")
                break
            
        logger.info(f"=== すべての処理が完了しました！ ===")

    except KeyboardInterrupt:
        logger.warning("ユーザーにより中断されました")
    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}", exc_info=True)

if __name__ == "__main__":
    run_automation()
