"""
TARGET自動化補助スクリプト
Power Automate for Desktopと連携して使用

機能:
1. 出力CSVファイルの確認と検証
2. ログファイルの生成
3. エラー通知
"""

import os
import glob
from datetime import datetime
import csv


class TargetOutputValidator:
    """TARGET出力CSVの検証クラス"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.log_dir = os.path.join(output_dir, 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
    
    def validate_latest_output(self):
        """最新の出力CSVを検証"""
        csv_files = glob.glob(os.path.join(self.output_dir, '*.CSV'))
        
        if not csv_files:
            self._log_error("CSVファイルが見つかりません")
            return False
        
        # 最新ファイルを取得
        latest_file = max(csv_files, key=os.path.getmtime)
        file_size = os.path.getsize(latest_file)
        
        print(f"✅ 最新ファイル: {os.path.basename(latest_file)}")
        print(f"   サイズ: {file_size:,} bytes")
        print(f"   更新日時: {datetime.fromtimestamp(os.path.getmtime(latest_file))}")
        
        # ファイル内容の検証
        try:
            with open(latest_file, 'r', encoding='shift_jis') as f:
                reader = csv.reader(f)
                header = next(reader)
                row_count = sum(1 for _ in reader)
            
            print(f"   データ行数: {row_count}")
            
            if row_count == 0:
                self._log_error(f"データが空です: {latest_file}")
                return False
            
            self._log_success(f"検証成功: {os.path.basename(latest_file)}, {row_count}行")
            return True
            
        except Exception as e:
            self._log_error(f"ファイル読み込みエラー: {e}")
            return False
    
    def list_all_outputs(self):
        """すべての出力ファイルをリスト表示"""
        csv_files = glob.glob(os.path.join(self.output_dir, '*.CSV'))
        
        if not csv_files:
            print("⚠️ CSVファイルが見つかりません")
            return
        
        print(f"\n📁 出力ファイル一覧 ({len(csv_files)}件)")
        print("-" * 80)
        
        for csv_file in sorted(csv_files, key=os.path.getmtime, reverse=True):
            filename = os.path.basename(csv_file)
            size = os.path.getsize(csv_file)
            mtime = datetime.fromtimestamp(os.path.getmtime(csv_file))
            
            print(f"{filename:30} {size:>10,} bytes  {mtime}")
    
    def _log_success(self, message: str):
        """成功ログを記録"""
        log_file = os.path.join(
            self.log_dir, 
            f"{datetime.now().strftime('%Y%m%d')}_success.log"
        )
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] SUCCESS: {message}\n")
    
    def _log_error(self, message: str):
        """エラーログを記録"""
        log_file = os.path.join(
            self.log_dir, 
            f"{datetime.now().strftime('%Y%m%d')}_error.log"
        )
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] ERROR: {message}\n")
        print(f"❌ エラー: {message}")


def main():
    """メイン処理"""
    import sys
    
    # 出力ディレクトリ
    output_dir = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'output'
    )
    output_dir = os.path.abspath(output_dir)
    
    validator = TargetOutputValidator(output_dir)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        # 一覧表示
        validator.list_all_outputs()
    else:
        # 最新ファイルの検証
        print("🔍 TARGET出力CSVの検証")
        print(f"📂 出力ディレクトリ: {output_dir}\n")
        
        success = validator.validate_latest_output()
        
        if success:
            print("\n✅ 検証完了")
            sys.exit(0)
        else:
            print("\n❌ 検証失敗")
            sys.exit(1)


if __name__ == '__main__':
    main()
