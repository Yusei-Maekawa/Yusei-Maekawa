import requests
import re
import sys

# ===== 設定値 =====
USERNAME = "Y_Maekawa"  # AtCoderのユーザー名
GOAL = 1200            # 目標レーティング
README_PATH = "README.md"  # 更新対象のファイル

print("=== AtCoder README Updater ===")
print(f"📊 設定情報:")
print(f"   - AtCoderユーザー名: {USERNAME}")
print(f"   - 目標レーティング: {GOAL}")
print(f"   - 更新ファイル: {README_PATH}")
print("")

def get_latest_rating(contest_type):
    """
    指定されたコンテストタイプの最新レーティングを取得
    
    Args:
        contest_type (str): "algorithm" または "heuristic"
    
    Returns:
        int: 最新のレーティング値（取得失敗時は0）
    """
    print(f"🔍 {contest_type.capitalize()} レーティング取得中...")
    
    try:
        # AtCoder APIのURL構築
        url = f"https://atcoder.jp/users/{USERNAME}/history/json?contestType={contest_type}"
        print(f"   📡 API URL: {url}")
        
        # APIリクエスト実行
        response = requests.get(url, timeout=10)
        print(f"   📶 レスポンス状況: {response.status_code}")
        
        # レスポンス検証
        if response.status_code != 200:
            print(f"   ❌ APIエラー: ステータスコード {response.status_code}")
            return 0
        
        if not response.text.strip():
            print(f"   ❌ 空のレスポンス")
            return 0
        
        # JSONデータ解析
        data = response.json()
        print(f"   📊 取得したコンテスト履歴数: {len(data)}")
        
        if not data:
            print(f"   ❌ コンテスト履歴が見つかりません")
            return 0
        
        # 最新のレーティングを取得（配列の最後の要素）
        latest_rating = data[-1]["NewRating"]
        print(f"   ✅ 最新レーティング: {latest_rating}")
        
        return latest_rating
        
    except requests.exceptions.Timeout:
        print(f"   ❌ タイムアウトエラー")
        return 0
    except requests.exceptions.RequestException as e:
        print(f"   ❌ リクエストエラー: {e}")
        return 0
    except (KeyError, IndexError) as e:
        print(f"   ❌ データ解析エラー: {e}")
        return 0
    except Exception as e:
        print(f"   ❌ 予期しないエラー: {e}")
        return 0

def calculate_remaining_points(current_rating, goal):
    """
    目標までの残りポイントを計算
    
    Args:
        current_rating (int): 現在のレーティング
        goal (int): 目標レーティング
    
    Returns:
        int: 残りポイント（既に達成している場合は0）
    """
    remaining = max(goal - current_rating, 0)
    
    if remaining == 0:
        print(f"   🎉 目標達成！現在のレーティング({current_rating})が目標({goal})を上回っています")
    else:
        print(f"   📈 残り{remaining}ポイントで目標達成")
    
    return remaining

def create_goal_section(algo_remain, heur_remain):
    """
    README.mdに挿入する目標セクションのHTMLを生成
    
    Args:
        algo_remain (int): Algorithm部門の残りポイント
        heur_remain (int): Heuristic部門の残りポイント
    
    Returns:
        str: 生成されたHTMLセクション
    """
    print(f"🎨 目標セクション生成中...")
    
    # 達成状況に応じた絵文字とメッセージ
    algo_status = "🎉 達成！" if algo_remain == 0 else f"残り {algo_remain} pt"
    heur_status = "🎉 達成！" if heur_remain == 0 else f"残り {heur_remain} pt"
    
    section = (
        f'<p align="center">\n'
        f'  <strong>📈 Algorithm Goal: {GOAL} — {algo_status}</strong><br>\n'
        f'  <strong>🧠 Heuristic Goal: {GOAL} — {heur_status}</strong>\n'
        f'</p>'
    )
    
    print(f"   ✅ セクション生成完了")
    print(f"   📝 生成内容:")
    for line in section.split('\n'):
        if line.strip():
            print(f"      {line}")
    
    return section

def update_readme_file(new_section):
    """
    README.mdファイルを更新
    
    Args:
        new_section (str): 挿入する新しいセクション
    
    Returns:
        bool: 更新成功の場合True
    """
    print(f"📝 README.md更新処理開始...")
    
    try:
        # ファイル読み込み
        print(f"   📖 {README_PATH} 読み込み中...")
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"   ✅ ファイル読み込み完了（{len(content)}文字）")
        
        # 更新対象セクションの検索パターン
        pattern = r'<!-- AtCoder Rating Goal Section: Do not edit below\. This will be auto-updated -->.*?<!-- End AtCoder Rating Goal Section -->'
        replacement = f'<!-- AtCoder Rating Goal Section: Do not edit below. This will be auto-updated -->\n{new_section}\n<!-- End AtCoder Rating Goal Section -->'
        
        print(f"   🔍 更新対象セクション検索中...")
        
        # パターンマッチング実行
        if re.search(pattern, content, re.DOTALL):
            print(f"   ✅ 更新対象セクション発見")
            print(f"   🔄 セクション置換実行中...")
            
            # 置換実行
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # ファイル書き込み
            print(f"   💾 ファイル書き込み中...")
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(updated_content)
            
            print(f"   ✅ ファイル更新完了")
            return True
            
        else:
            print(f"   ❌ 更新対象セクションが見つかりません")
            print(f"   🔍 デバッグ: 'AtCoder Rating Goal' を含む行を検索...")
            
            lines = content.split('\n')
            found_lines = []
            for i, line in enumerate(lines):
                if 'AtCoder Rating Goal' in line:
                    found_lines.append(f"      行{i+1}: {line}")
            
            if found_lines:
                print(f"   📋 関連する行が見つかりました:")
                for line in found_lines:
                    print(line)
            else:
                print(f"   ❌ 関連する行が見つかりませんでした")
                print(f"   💡 README.mdに以下のコメントセクションを追加してください:")
                print(f"      <!-- AtCoder Rating Goal Section: Do not edit below. This will be auto-updated -->")
                print(f"      <!-- End AtCoder Rating Goal Section -->")
            
            return False
    
    except FileNotFoundError:
        print(f"   ❌ エラー: {README_PATH} が見つかりません")
        return False
    except Exception as e:
        print(f"   ❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    メイン処理の実行
    """
    print("🚀 処理開始\n")
    
    try:
        # === ステップ1: レーティング取得 ===
        print("=" * 50)
        print("📊 STEP 1: AtCoderレーティング取得")
        print("=" * 50)
        
        # Algorithm部門のレーティング取得
        algo_rating = get_latest_rating("algorithm")
        print("")
        
        # Heuristic部門のレーティング取得
        heur_rating = get_latest_rating("heuristic")
        print("")
        
        # === ステップ2: 残りポイント計算 ===
        print("=" * 50)
        print("🧮 STEP 2: 残りポイント計算")
        print("=" * 50)
        
        print(f"📈 Algorithm部門:")
        print(f"   現在: {algo_rating} pt")
        print(f"   目標: {GOAL} pt")
        algo_remain = calculate_remaining_points(algo_rating, GOAL)
        print("")
        
        print(f"🧠 Heuristic部門:")
        print(f"   現在: {heur_rating} pt")
        print(f"   目標: {GOAL} pt")
        heur_remain = calculate_remaining_points(heur_rating, GOAL)
        print("")
        
        # === ステップ3: HTMLセクション生成 ===
        print("=" * 50)
        print("🎨 STEP 3: 目標セクション生成")
        print("=" * 50)
        
        new_section = create_goal_section(algo_remain, heur_remain)
        print("")
        
        # === ステップ4: README.md更新 ===
        print("=" * 50)
        print("📝 STEP 4: README.md更新")
        print("=" * 50)
        
        success = update_readme_file(new_section)
        print("")
        
        # === 結果表示 ===
        print("=" * 50)
        print("📋 実行結果")
        print("=" * 50)
        
        if success:
            print("✅ README.md更新成功！")
            print(f"📊 更新内容:")
            print(f"   - Algorithm: {algo_rating}pt (残り{algo_remain}pt)")
            print(f"   - Heuristic: {heur_rating}pt (残り{heur_remain}pt)")
        else:
            print("❌ README.md更新失敗")
            print("💡 上記のエラーメッセージを確認してください")
    
    except Exception as e:
        print("=" * 50)
        print("❌ 致命的エラー")
        print("=" * 50)
        print(f"エラー内容: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("\n" + "=" * 50)
    print("🏁 スクリプト実行完了")
    print("=" * 50)
