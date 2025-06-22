# scripts/update_badges.py
import re
import requests

def get_rating(contest_type):
    try:
        url = f"https://atcoder.jp/users/Y_Maekawa/history/json?contestType={contest_type}"
        res = requests.get(url, timeout=10)
        
        # HTTPステータスコードをチェック
        if res.status_code != 200:
            print(f"HTTP Error {res.status_code} for {contest_type}")
            print(f"Response content: {res.text[:200]}")
            return 0
        
        # レスポンスが空でないかチェック
        if not res.text.strip():
            print(f"Empty response for {contest_type}")
            return 0
        
        # JSONとしてパース
        data = res.json()
        
        if not data:
            print(f"No data found for {contest_type}")
            return 0
        
        # 最新のレーティングを取得
        return data[-1]["NewRating"]
        
    except requests.exceptions.RequestException as e:
        print(f"Request error for {contest_type}: {e}")
        return 0
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error for {contest_type}: {e}")
        print(f"Response content: {res.text[:200]}")
        return 0
    except (KeyError, IndexError) as e:
        print(f"Data parsing error for {contest_type}: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error for {contest_type}: {e}")
        return 0

def replace_badges(content):
    try:
        print("Getting algorithm rating...")
        algo_rating = get_rating("algorithm")
        print(f"Algorithm rating: {algo_rating}")
        
        print("Getting heuristic rating...")
        heuristic_rating = get_rating("heuristic")
        print(f"Heuristic rating: {heuristic_rating}")
        
        # バッジのURL生成
        algo_badge_url = f"https://img.shields.io/badge/AtCoder-{algo_rating}-brightgreen"
        heuristic_badge_url = f"https://img.shields.io/badge/AtCoder_Heuristic-{heuristic_rating}-brightgreen"
        
        # バッジの置換
        content = re.sub(
            r'!\[AtCoder\]\(https://img\.shields\.io/badge/AtCoder-\d+-brightgreen\)',
            f'![AtCoder]({algo_badge_url})',
            content
        )
        
        content = re.sub(
            r'!\[AtCoder Heuristic\]\(https://img\.shields\.io/badge/AtCoder_Heuristic-\d+-brightgreen\)',
            f'![AtCoder Heuristic]({heuristic_badge_url})',
            content
        )
        
        return content
        
    except Exception as e:
        print(f"Error in replace_badges: {e}")
        return content

if __name__ == "__main__":
    try:
        print("Reading README.md...")
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        print("Updating badges...")
        updated = replace_badges(content)
        
        print("Writing updated README.md...")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated)
        
        print("Badge update completed successfully!")
        
    except FileNotFoundError:
        print("Error: README.md not found")
    except Exception as e:
        print(f"Unexpected error: {e}")
