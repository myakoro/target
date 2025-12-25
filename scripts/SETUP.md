# TARGET時系列オッズ自動取得 - セットアップガイド

## 必要な環境

- Windows 10/11
- Python 3.8以上
- TARGETソフトウェア（インストール済み）

## セットアップ手順

### 1. Pythonライブラリのインストール

```powershell
cd "C:\Users\takuy\Desktop\投資競馬アプリ系\target系\scripts"
pip install pyautogui pillow pygetwindow
```

### 2. 座標キャリブレーション（初回のみ）

TARGETの画面要素の座標を記録します。

```powershell
python target_automation.py --calibrate
```

**操作手順:**
1. TARGETを起動し、メインウィンドウを表示
2. スクリプト実行後、5秒以内に以下の要素を順番にクリック:
   - レース検索メニュー
   - 開始日入力フィールド
   - 終了日入力フィールド
   - 検索ボタン
   - 全選択ボタン
   - 時系列オッズダウンロードメニュー
   - CSV出力ボタン
3. 座標が `coords.json` に保存されます

### 3. 自動取得の実行

```powershell
# 例: 2024年1月のデータを取得
python target_automation.py --start-date 2024-01-01 --end-date 2024-01-31
```

**パラメータ:**
- `--start-date`: 開始日（YYYY-MM-DD形式）
- `--end-date`: 終了日（YYYY-MM-DD形式）
- `--output-dir`: 出力先（省略時: `../output`）

## 使用上の注意

### 実行前の確認事項
- [ ] TARGETが起動している
- [ ] TARGETウィンドウが最前面に表示されている
- [ ] 座標キャリブレーションが完了している

### 実行中の注意
- ⚠️ **実行中はマウス・キーボードを操作しないでください**
- ⚠️ 緊急停止: マウスを画面左上隅に移動

### トラブルシューティング

#### 座標がずれる場合
- ディスプレイ解像度やウィンドウサイズが変わると座標がずれます
- 再度キャリブレーションを実行してください

#### クリックが反応しない
- TARGETウィンドウが最前面にあるか確認
- `pyautogui.PAUSE` の値を増やして待機時間を延長

#### ダウンロードが完了しない
- レース数が多い場合、ダウンロード時間が長くなります
- スクリプト内の `time.sleep(10)` を調整

## 代替案: Power Automate for Desktop

より安定した自動化には、Microsoft Power Automate for Desktop（無料）の使用を推奨します。

### 利点
- GUIベースで操作を記録
- 画像認識による要素検出
- エラーハンドリングが充実

### 使用方法
1. Power Automate for Desktopを起動
2. 「新しいフロー」を作成
3. 「レコーダー」機能で操作を記録
4. 記録したフローを編集・保存
5. スケジュール実行設定

## ファイル構成

```
scripts/
├── target_automation.py    # 自動化スクリプト
├── coords.json            # 座標設定（自動生成）
└── SETUP.md              # このファイル
```

## 次のステップ

1. ✅ セットアップ完了
2. ⬜ 座標キャリブレーション実行
3. ⬜ テスト実行（短期間で試す）
4. ⬜ 本番実行
5. ⬜ 定期実行の設定（タスクスケジューラ等）
