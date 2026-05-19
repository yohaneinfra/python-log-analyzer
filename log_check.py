import sys
import requests
import os
from datetime import datetime


# 引数があるかチェック
if len(sys.argv) >= 2:
    target_date = sys.argv[1]
else:
    target_date = datetime.now().strftime("%Y-%m-%d")

print("対象日付:", target_date)


def send_slack(message):

    webhook_url = os.getenv("SLACK_WEBFHOOK_URL")
    
    
    if not webhook_url:
        print("webhook urlが設定されていません")
        return
        
        
    payload = {
        "text": message
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Slackに通知しました")
    
    except Exception as e:
        print("Slack送信エラー:", e)

def check_log(target_date):

    # 監視対象のログファイル一覧
    log_files = ["access.log", "error.log"]

    # 件数カウント用の変数
    error_count = 0
    warning_count = 0

    try:
        with open("result.log", "w", encoding="utf-8") as out:

            out.write(f"{target_date} の結果\n")
            out.write("---------------------\n")

            # 複数のログファイルを順番に処理する
            for log_file in log_files:

                out.write(f"\n対象ファイル: {log_file}\n")
                out.write("---------------------\n")

                try:
                    with open(log_file, "r", encoding="utf-8") as file:

                        for line in file:

                            # 対象日付じゃなければスキップ
                            if target_date not in line:
                                continue

                            # ERRORの場合
                            if "ERROR" in line:
                                print(f"{log_file}: {line.strip()}")
                                out.write("[ERROR] " + line)
                                error_count += 1

                            # WARNINGの場合
                            elif "WARNING" in line:
                                print(f"{log_file}: {line.strip()}")
                                out.write("[WARNING] " + line)
                                warning_count += 1

                except FileNotFoundError:
                    out.write(f"{log_file} が見つかりません\n")
                    print(f"{log_file} が見つかりません")

            out.write("\n")
            out.write("-------------------------\n")
            out.write(f"ERRORの件数: {error_count}\n")
            out.write(f"WARNINGの件数: {warning_count}\n")

        print("result.log に出力しました。")
        
        if error_count > 0:
            send_slack(
                f"ログ監視アラート\n"
                f"日付: {target_date}\n"
                f"ERROR: {error_count}件\n"
                f"WARNING: {warning_count}件\n"
            )

    except PermissionError:
        print("ファイルの読み書き権限がありません")

    except Exception as e:
        print("予期しないエラーが発生しました:", e)


# 関数を実行
check_log(target_date)