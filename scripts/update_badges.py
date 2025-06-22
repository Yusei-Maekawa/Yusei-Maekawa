# scripts/update_badges.py
import re
import requests

def get_rating(contest_type):
    try:
        url = f"https://atcoder.jp/users/Y_Maekawa/history/json?contestType={contest_type}"
        res = requests.get(url, timeout=10)
        
        if res.status_code != 200:
            print(f"HTTP Error {res.status_code} for {contest_type}")
            return 0
        
        if not res.text.strip():
            print(f"Empty response for {contest_type}")
            return 0
        
        data = res.json()
        
        if not data:
            print(f"No data found for {contest_type}")
            return 0
        
        # 最新のレーティングを取得
        latest_rating = data[-1]["NewRating"]
        print(f"Latest rating for {contest_type}: {latest_rating}")
        return latest_rating
        
    except Exception as e:
        print(f"Error for {contest_type}: {e}")
        return 0

def get_badge_color(rating):
    """レーティングに応じた色を返す"""
    if rating >= 2800:
        return "red"
    elif rating >= 2400:
        return "orange"
    elif rating >= 2000:
        return "yellow"
    elif rating >= 1600:
        return "blue"
    elif rating >= 1200:
        return "lightblue"
    elif rating >= 800:
        return "green"
    elif rating >= 400:
        return "brown"
    else:
        return "gray"

def replace_badges(content):
    try:
        print("Getting algorithm rating...")
        algo_rating = get_rating("algorithm")
        
        print("Getting heuristic rating...")
        heuristic_rating = get_rating("heuristic")
        
        # バッジの色を決定
        algo_color = get_badge_color(algo_rating)
        heuristic_color = get_badge_color(heuristic_rating)
        
        print(f"Algorithm rating: {algo_rating}, color: {algo_color}")
        print(f"Heuristic rating: {heuristic_rating}, color: {heuristic_color}")
        
        # README.mdの実際の形式に合わせた置換
        # Algorithm バッジの置換
        algo_pattern = r'<img src="https://img\.shields\.io/badge/Algorithm-[^"]*" alt="Algorithm Rating">'
        new_algo_badge = f'<img src="https://img.shields.io/badge/Algorithm-{algo_rating}-{algo_color}" alt="Algorithm Rating">'
        content = re.sub(algo_pattern, new_algo_badge, content)
        
        # Heuristic バッジの置換
        heuristic_pattern = r'<img src="https://img\.shields\.io/badge/Heuristic-[^"]*" alt="Heuristic Rating">'
        new_heuristic_badge = f'<img src="https://img.shields.io/badge/Heuristic-{heuristic_rating}-{heuristic_color}" alt="Heuristic Rating">'
        content = re.sub(heuristic_pattern, new_heuristic_badge, content)
        
        print(f"New algorithm badge: {new_algo_badge}")
        print(f"New heuristic badge: {new_heuristic_badge}")
        
        return content
        
    except Exception as e:
        print(f"Error in replace_badges: {e}")
        return content

if __name__ == "__main__":
    try:
        print("Reading README.md...")
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        print("Current content preview:")
        # バッジの行を探して表示
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if ('Algorithm' in line or 'Heuristic' in line) and 'shields.io' in line:
                print(f"Line {i+1}: {line}")
        
        print("\nUpdating badges...")
        updated = replace_badges(content)
        
        print("Writing updated README.md...")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated)
        
        print("Badge update completed successfully!")
        
        # 更新後の確認
        print("\nUpdated content preview:")
        lines = updated.split('\n')
        for i, line in enumerate(lines):
            if ('Algorithm' in line or 'Heuristic' in line) and 'shields.io' in line:
                print(f"Line {i+1}: {line}")
        
    except Exception as e:
        print(f"Error: {e}")
