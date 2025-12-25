from PIL import Image
import os

# 1. レース一覧ヘッダー (Race Header)
source_path_header = r"C:/Users/takuy/.gemini/antigravity/brain/8de6bc59-c24d-48fd-b90a-d29bda30e38f/uploaded_image_1765726362544.png"
dest_path_header = r"C:\Users\takuy\Desktop\投資競馬アプリ系\target系\scripts\race_header_ref.png"

if os.path.exists(source_path_header):
    try:
        img = Image.open(source_path_header)
        # 「R レース名」の文字部分だけを狙う (左上)
        # 元画像はリスト全体。左上隅にヘッダーがあるはず。
        # 余白を排除し、文字だけを含むように crop
        header_crop = img.crop((2, 2, 80, 20)) 
        header_crop.save(dest_path_header)
        print(f"Saved header ref to {dest_path_header}")
    except Exception as e:
        print(f"Error header: {e}")

# 2. オッズボタン (Odds Button)
source_path_odds = r"C:/Users/takuy/.gemini/antigravity/brain/8de6bc59-c24d-48fd-b90a-d29bda30e38f/uploaded_image_1765727563475.png"
dest_path_odds = r"C:\Users\takuy\Desktop\投資競馬アプリ系\target系\scripts\odds_btn_ref.png"

if os.path.exists(source_path_odds):
    try:
        img = Image.open(source_path_odds)
        # そのまま保存（ユーザー提供画像がボタンそのもの）
        img.save(dest_path_odds)
        print(f"Saved odds ref to {dest_path_odds}")
    except Exception as e:
        print(f"Error odds: {e}")
