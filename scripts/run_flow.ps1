# Power Automate for Desktop フロー起動スクリプト
# コマンドラインから日付を指定してフローを実行

param(
    [Parameter(Mandatory=$true)]
    [string]$StartDate,
    
    [Parameter(Mandatory=$true)]
    [string]$EndDate,
    
    [string]$FlowName = "TARGET時系列オッズ自動取得"
)

# 日付形式の検証
try {
    $start = [DateTime]::ParseExact($StartDate, "yyyy-MM-dd", $null)
    $end = [DateTime]::ParseExact($EndDate, "yyyy-MM-dd", $null)
    
    # YYYY/MM/DD形式に変換
    $startFormatted = $start.ToString("yyyy/MM/dd")
    $endFormatted = $end.ToString("yyyy/MM/dd")
    
    Write-Host "📅 実行期間: $startFormatted ～ $endFormatted" -ForegroundColor Cyan
} catch {
    Write-Host "❌ エラー: 日付はYYYY-MM-DD形式で指定してください" -ForegroundColor Red
    Write-Host "   例: .\run_flow.ps1 -StartDate 2024-12-01 -EndDate 2024-12-31"
    exit 1
}

# Power Automate for Desktop の実行
Write-Host "`n🚀 Power Automate フローを起動します..." -ForegroundColor Green
Write-Host "   フロー名: $FlowName"

# PAD.Console.Host.exe のパスを検索
$padPath = Get-ChildItem -Path "C:\Program Files (x86)\Power Automate Desktop" -Filter "PAD.Console.Host.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $padPath) {
    Write-Host "❌ エラー: Power Automate Desktop が見つかりません" -ForegroundColor Red
    Write-Host "   Power Automate for Desktop がインストールされているか確認してください"
    exit 1
}

# フローを実行
$variables = "StartDate:$startFormatted,EndDate:$endFormatted"

try {
    Write-Host "`n⏳ 実行中..." -ForegroundColor Yellow
    
    & $padPath.FullName /run $FlowName /variables $variables
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ フロー実行完了" -ForegroundColor Green
        
        # 出力検証
        Write-Host "`n🔍 出力CSVを検証中..."
        python "$PSScriptRoot\validate_output.py"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ すべて完了しました！" -ForegroundColor Green
        } else {
            Write-Host "`n⚠️ 出力検証でエラーが発生しました" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n❌ フロー実行でエラーが発生しました" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "`n❌ エラー: $_" -ForegroundColor Red
    exit 1
}
