import pyautogui
import time
import sys
import json
import logging
import os
from datetime import datetime

# ロギング設定
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, f'automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# PyAutoGUI設定
pyautogui.FAILSAFE = True  # マウスを左上に持っていくと強制終了
pyautogui.PAUSE = 1.0     # 各操作後の待機時間

# 座標定義 (1920x1080 最大化時)
COORDS = {
    'seiseki_btn': (80, 150),      # 成績ボタン
    'kai_name_tab': (450, 95),     # 開催名タブ
    'year_select': (240, 95),      # 年度選択プルダウン
    
    # 開催日一覧 (1行目から順に下へ)
    'venue_list_start': (200, 140), # 開催日一覧の1行目 (修正: 少し下へ)
    'venue_row_height': 16,        # 行の高さ
    
    # レース一覧 (1行目から順に下へ)
    'race_list_start': (67, 210),  # レース一覧の1行目 (ユーザー環境キャリブレーション済み)
    'race_row_height': 16,         # 行の高さ
    
    # オッズ画面操作
    'odds_btn': (771, 119),        # オッズボタン (ユーザー環境キャリブレーション済み)
    'jikei_tab': (963, 140),       # 単複時系タブ (ユーザー環境キャリブレーション済み)
    'jv_get_btn': (324, 117),      # JVオッズ取得ボタン (ユーザー環境キャリブレーション済み)
    
    # CSV出力メニュー
    'file_menu': (35, 35),         # ファイルメニュー (Alt+Fで代用可)
    'text_out_menu': (100, 250),   # テキストファイル出力 (想定位置)
    'csv_format_menu': (300, 250), # CSV形式 (想定位置)
    
    # ダイアログ操作
    'ok_btn': (960, 600),          # OKボタン (ダイアログ中央想定)
    'close_btn': (1900, 10),       # 閉じるボタン（右上）
    'close_btn_2': (1870, 10)      # 2つ目の閉じるボタン（少し左）
}

# --- キャリブレーション座標の読み込み ---
CALIBRATED_COORDS = {}
coords_file = os.path.join(os.path.dirname(__file__), 'target_coords.json')
if os.path.exists(coords_file):
    try:
        with open(coords_file, 'r') as f:
            CALIBRATED_COORDS = json.load(f)
        logger.info(f"Loaded calibrated coordinates: {CALIBRATED_COORDS}")
    except Exception as e:
        logger.error(f"Failed to load coordinates: {e}")

def click_wait(x, y, wait=1.0, description=""):
    """指定座標をクリックして待機"""
    logger.info(f"Clicking: {description} at ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(wait)

def select_item_by_keys(x, y, down_count=0, description="", wait=1.0, reset_key=None, reset_presses=1, do_focus_click=True):
    """指定座標をクリックしてフォーカスし、矢印キーで選択してEnter"""
    logger.info(f"Key Nav: {description} (Reset={reset_key}x{reset_presses} -> Down={down_count}, Click={do_focus_click})")
    
    # 1. リストをクリックしてフォーカス (必要な場合のみ)
    if do_focus_click:
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
    else:
        logger.info("Skipping mouse focus click.")
    
    # 2. リセットキー押下 (例: up連打で先頭へ)
    if reset_key:
        pyautogui.press(reset_key, presses=reset_presses, interval=0.05)
        time.sleep(0.2)
    
    # 3. 指定回数だけ下へ
    if down_count > 0:
        pyautogui.press('down', presses=down_count, interval=0.1)
        time.sleep(0.2)
        
    # 4. Enterで決定
    pyautogui.press('enter')
    logger.info(f"Waiting {wait}s for transition...")
    time.sleep(wait) # 画面遷移待ち

def double_click_wait(x, y, wait=1.0, description=""):
    """(非推奨) 指定座標をクリックしてEnterキー送信"""
    # 既存コードとの互換性のため残すが、select_item_by_keys推奨
    select_item_by_keys(x, y, 0, description, wait)
    time.sleep(wait)

def process_one_race(race_idx):
    """1レース分の処理"""
    logger.info(f"--- Processing Race {race_idx + 1} ---")
    
    # 1. レース選択
    # 優先順位: キャリブレーション > 画像認識 > 固定座標
    
    target_pos = None
    use_calibrated = False
    
    if 'race_list_1r' in CALIBRATED_COORDS:
        target_pos = CALIBRATED_COORDS['race_list_1r']
        logger.info(f"Using calibrated Race 1 pos: {target_pos}")
        use_calibrated = True
    else:
        # 画像認識 (キャリブレーションがない場合)
        header_img_path = os.path.join(os.path.dirname(__file__), 'race_header_ref.png')
        if os.path.exists(header_img_path):
            try:
                # 画面上からヘッダーを探す (confidenceなし: 完全一致)
                logger.info("Locating race list header...")
                location = pyautogui.locateOnScreen(header_img_path)
                
                if location:
                    logger.info(f"Header found at: {location}")
                    target_x = location.left + 20
                    target_y = location.top + location.height + 10
                    target_pos = (target_x, target_y)
            except Exception:
                pass

    if target_pos:
        race_list_x, race_list_y = target_pos
    else:
        race_list_x, race_list_y = COORDS['race_list_start'] # 固定座標呼び出し
        # 確実にリスト内(1行目中央付近)をクリックするため座標を直接指定
        race_list_x, race_list_y = 100, 160
    
    # レース選択実行
    select_item_by_keys(race_list_x, race_list_y, 
                        down_count=race_idx, 
                        description=f"Race {race_idx+1}", 
                        wait=3.0, 
                        reset_key='home',   # Homeキーで確実に1Rへ
                        reset_presses=1,
                        do_focus_click=True
                        )
    
    # 2. オッズボタン
    odds_x, odds_y = COORDS['odds_btn']
    odds_desc = "Odds Button (Fixed)"
    odds_clicked = False
    
    if 'odds_btn' in CALIBRATED_COORDS:
        odds_x, odds_y = CALIBRATED_COORDS['odds_btn']
        odds_desc = "Odds Button (Calibrated)"
        click_wait(odds_x, odds_y, wait=2.0, description=odds_desc)
    else:
        # 画像認識 (キャリブレーションがない場合)
        odds_btn_path = os.path.join(os.path.dirname(__file__), 'odds_btn_ref.png')
        if os.path.exists(odds_btn_path):
            try:
                logger.info("Locating Odds button...")
                odds_loc = pyautogui.locateOnScreen(odds_btn_path)
                if odds_loc:
                    center = pyautogui.center(odds_loc)
                    click_wait(center.x, center.y, wait=2.0, description="Odds Button (Image)")
                    odds_clicked = True
            except Exception:
                pass
        
        if not odds_clicked:
             click_wait(odds_x, odds_y, wait=2.0, description=odds_desc)
    
    # 3. 単複時系タブ
    jikei_x, jikei_y = COORDS['jikei_tab']
    jikei_desc = "Jikei Tab (Fixed)"
    if 'jikei_tab' in CALIBRATED_COORDS:
        jikei_x, jikei_y = CALIBRATED_COORDS['jikei_tab']
        jikei_desc = "Jikei Tab (Calibrated)"
        
    click_wait(jikei_x, jikei_y, wait=2.0, description=jikei_desc)
    
    # 4. JVオッズ取得
    jv_x, jv_y = COORDS['jv_get_btn']
    jv_desc = "JV Get Button (Fixed)"
    if 'jv_get_btn' in CALIBRATED_COORDS:
        jv_x, jv_y = CALIBRATED_COORDS['jv_get_btn']
        jv_desc = "JV Get Button (Calibrated)"
        
    click_wait(jv_x, jv_y, wait=30.0, description=f"{jv_desc} (Waiting 30s)")
    
    # 5. CSV出力 (Alt+F -> T -> C のショートカット使用推奨)
    logger.info("Exporting CSV...")
    pyautogui.hotkey('alt', 'f')
    time.sleep(1.0)
    pyautogui.press('t') # テキストファイル出力
    time.sleep(1.0)
    pyautogui.press('c') # 単複時系列オッズCSV形式
    time.sleep(1.0)
    
    # 6. OKボタン (Enterで代用)
    logger.info("Pressing OK...")
    pyautogui.press('enter')
    time.sleep(2.0) # 保存待ち
    
    # 7. 閉じる x 2 (Escで戻る方が安全かも？)
    logger.info("Closing windows...")
    pyautogui.hotkey('alt', 'f4') # 閉じる
    time.sleep(1.0)
    pyautogui.hotkey('alt', 'f4') # もう一度閉じる
    time.sleep(1.0)

def main():
    logger.info("Starting TARGET Automation...")
    logger.info("Please maximize TARGET window and bring it to front.")
    logger.info("Automation will start in 5 seconds...")
    time.sleep(5)
    
    # 1. 開催日タブへ移動 (手動でそこまで行っている前提ならスキップ可)
    # ここでは、既に開催日一覧が表示されている状態からスタートと仮定
    
    # テスト: 最初の1開催日のみ処理
    venue_idx = 0
    # 開催日リストもキーボード選択に変更
    venue_list_x, venue_list_y = COORDS['venue_list_start']
    
    select_item_by_keys(venue_list_x, venue_list_y, down_count=venue_idx, description=f"Venue {venue_idx+1}", wait=5.0)
    
    # レースループ (12レース)
    for i in range(12):
        try:
            process_one_race(i)
        except Exception as e:
            logger.error(f"Error in race {i+1}: {e}")
            # エラー時はEsc連打で戻るなどを検討
            pyautogui.press('esc', presses=3, interval=0.5)
            continue
            
    logger.info("Automation Completed!")

if __name__ == "__main__":
    main()
