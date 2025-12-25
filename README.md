# TARGET時系列オッズ自動取得システム

## 目的
TARGETソフトウェアから日付範囲を指定して時系列オッズデータを自動取得し、CSV形式で出力する。

## 自動化アプローチ

### フェーズ1: 半自動化（TARGET内蔵機能活用）
TARGETの標準機能を使った手動操作手順を確立。

#### 手順
1. TARGETを起動
2. レース検索画面で日付範囲を指定（例: 2024/01/01 - 2024/01/31）
3. 検索実行 → 全レース選択
4. ファイルメニュー → 「時系列オッズのダウンロード」
5. 出馬表レース選択画面 → CSV一括出力
6. 指定フォルダに出力

#### 設定
- 環境設定 → 「時系列オッズCSV形式出力用フォルダ」を `C:\Users\takuy\Desktop\投資競馬アプリ系\target系\output` に設定

### フェーズ2: 完全自動化（RPA活用）
Power Automate for Desktop / UiPath / WinActorでUI操作を自動化。

#### 自動化対象
- TARGETの起動
- レース検索条件の入力（日付範囲）
- 検索実行とレース選択
- 時系列オッズダウンロード
- CSV出力
- TARGETの終了

## ファイル構成

```
target系/
├── README.md                    # このファイル
├── output/                      # TARGET CSV出力先
├── scripts/
│   ├── target_automation.py     # Python自動化スクリプト（PyAutoGUI使用）
│   └── target_automation.ps1    # PowerShell補助スクリプト
└── rpa/
    └── target_flow.json         # Power Automate フロー定義
```

## 必要な情報

### TARGET操作手順の詳細確認が必要
1. レース検索画面の正確なメニューパス
2. 日付範囲指定の入力フィールド位置
3. 時系列オッズダウンロードボタンの位置
4. CSV出力時の設定項目

## 次のステップ

1. ✅ TARGET機能調査完了
2. ⬜ 手動操作手順の詳細確認とスクリーンショット取得
3. ⬜ Power Automate for Desktop フロー作成
4. ⬜ Python補助スクリプト作成（ファイル管理等）
5. ⬜ 動作テストと検証
