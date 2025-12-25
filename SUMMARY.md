# TARGET時系列オッズ自動取得システム - 実装サマリー

## 📋 プロジェクト概要

TARGETソフトウェアから日付範囲を指定して単複時系列オッズデータを自動取得し、CSV形式で出力するシステム。

**目的:** 手動操作の自動化により、効率的なデータ収集を実現

## 🎯 実装アプローチ

### 方法1: Python + PyAutoGUI（軽量・簡易）
- **難易度:** ⭐⭐⭐
- **安定性:** ⭐⭐
- **推奨度:** 中

### 方法2: Power Automate for Desktop（推奨）
- **難易度:** ⭐⭐
- **安定性:** ⭐⭐⭐⭐
- **推奨度:** 高

### 方法3: WinActor（商用）
- **難易度:** ⭐⭐
- **安定性:** ⭐⭐⭐⭐⭐
- **推奨度:** 中（ライセンス必要）

## 📁 ファイル構成

```
target系/
├── README.md                      # プロジェクト概要
├── MANUAL_PROCEDURE.md            # 手動操作手順（詳細）
├── JD07255101.CSV                 # サンプルデータ
│
├── output/                        # CSV出力先
│   └── (自動生成されるCSVファイル)
│
├── screenshots/                   # 画面キャプチャ保存先
│   └── (手動で追加)
│
├── scripts/                       # Python自動化
│   ├── SETUP.md                   # セットアップガイド
│   ├── target_automation.py       # 自動化スクリプト
│   └── coords.json                # 座標設定（自動生成）
│
└── rpa/                           # RPA関連
    └── FLOW_DESIGN.md             # Power Automate設計書
```

## 🚀 クイックスタート

### 方法1: Python自動化

#### 1. セットアップ
```powershell
cd "C:\Users\takuy\Desktop\投資競馬アプリ系\target系\scripts"
pip install pyautogui pillow pygetwindow
```

#### 2. 座標キャリブレーション
```powershell
python target_automation.py --calibrate
```

#### 3. 実行
```powershell
python target_automation.py --start-date 2024-01-01 --end-date 2024-01-31
```

### 方法2: Power Automate for Desktop（推奨）

#### 1. Power Automate起動
- Windowsスタートメニューから起動（無料）

#### 2. フロー作成
- 「新しいフロー」作成
- 「デスクトップレコーダー」で操作を記録
- `MANUAL_PROCEDURE.md` の手順に従って操作

#### 3. フロー編集
- 変数を入力パラメータに変更
- エラーハンドリング追加
- `rpa/FLOW_DESIGN.md` を参照

#### 4. 実行
- フローを保存して実行
- スケジュール設定で定期実行可能

## 📊 取得データ形式

### CSVファイル（Shift-JIS、横持ち形式）

```csv
レースID,区分,月日時分,頭数,単勝票数,複勝票数,1単,1複Lo,1複Hi,2単,2複Lo,2複Hi,...
2024010607010101,1,01061000,16,100,200,3.5,1.2,1.5,8.2,2.1,3.0,...
```

### データ項目
- **レースID**: 年月日場R（12桁）
- **月日時分**: タイムスタンプ（MMDDHHmm）
- **N単**: N番馬の単勝オッズ
- **N複Lo/Hi**: N番馬の複勝オッズ範囲

## ⚙️ TARGET環境設定

### 必須設定
1. TARGET起動
2. `環境設定` → `各種設定`
3. `時系列オッズCSV形式出力用フォルダ` を設定:
   ```
   C:\Users\takuy\Desktop\投資競馬アプリ系\target系\output
   ```

## 📝 手動操作手順（概要）

1. **レース検索** → 日付範囲指定
2. **検索実行** → 全レース選択
3. **時系列オッズダウンロード** （数分～数十分）
4. **CSV一括出力** → 完了

詳細は `MANUAL_PROCEDURE.md` を参照

## ⏱️ 所要時間の目安

| データ量 | ダウンロード | CSV出力 | 合計 |
|---------|------------|---------|------|
| 1日分（36R） | 2-5分 | 10-30秒 | 3-6分 |
| 1週間（250R） | 10-20分 | 1-2分 | 12-22分 |
| 1ヶ月（1000R） | 30-60分 | 3-5分 | 35-65分 |

## 🔧 トラブルシューティング

### Python版
- **座標がずれる** → 再キャリブレーション
- **クリックが反応しない** → 待機時間を延長
- **緊急停止** → マウスを画面左上隅へ

### Power Automate版
- **UI要素が見つからない** → セレクター再取得
- **タイムアウト** → 待機時間を延長
- **エラーログ** → `output/logs/` を確認

## 📚 ドキュメント一覧

| ファイル | 内容 | 対象者 |
|---------|------|--------|
| `README.md` | プロジェクト概要 | 全員 |
| `SUMMARY.md` | 実装サマリー（このファイル） | 全員 |
| `MANUAL_PROCEDURE.md` | 手動操作手順 | 全員 |
| `scripts/SETUP.md` | Python版セットアップ | 開発者 |
| `scripts/target_automation.py` | Python自動化スクリプト | 開発者 |
| `rpa/FLOW_DESIGN.md` | Power Automate設計書 | RPA担当者 |

## 🎓 学習リソース

### Power Automate for Desktop
- [公式ドキュメント](https://learn.microsoft.com/ja-jp/power-automate/desktop-flows/)
- [UI自動化ベストプラクティス](https://learn.microsoft.com/ja-jp/power-automate/desktop-flows/ui-automation-best-practices)

### PyAutoGUI
- [公式ドキュメント](https://pyautogui.readthedocs.io/)

## 🔄 次のステップ

### Phase 1: 手動操作の習熟
- [ ] `MANUAL_PROCEDURE.md` に従って手動操作を実施
- [ ] 操作画面のスクリーンショットを `screenshots/` に保存
- [ ] 所要時間を計測

### Phase 2: 自動化の実装
- [ ] **推奨:** Power Automate for Desktopでフロー作成
- [ ] または: Python版で座標キャリブレーション
- [ ] 短期間（1日分）でテスト実行

### Phase 3: 本番運用
- [ ] 長期間のデータ取得
- [ ] エラーハンドリングの強化
- [ ] スケジュール実行の設定

### Phase 4: データ活用
- [ ] 取得したCSVデータを分析アプリに統合
- [ ] データベースへのインポート処理
- [ ] 可視化・レポート作成

## 💡 推奨事項

1. **まずPower Automate for Desktopを試す**
   - Windows標準、無料、安定性が高い
   - GUIベースで直感的

2. **手動操作を完全に理解してから自動化**
   - トラブル時の対処が容易

3. **小規模テストから開始**
   - 1日分のデータで動作確認
   - 徐々に規模を拡大

4. **エラーログを必ず記録**
   - 問題発生時の原因特定に必須

## 📞 サポート

質問や問題が発生した場合:
1. 該当ドキュメントのトラブルシューティングセクションを確認
2. エラーログを確認
3. スクリーンショットを撮影して状況を記録

## 📅 更新履歴

| 日付 | バージョン | 更新内容 |
|------|-----------|---------|
| 2024-12-14 | v1.0 | 初版作成 |

---

**作成日:** 2024-12-14  
**プロジェクト:** 投資競馬アプリ系  
**目的:** TARGET時系列オッズ自動取得
