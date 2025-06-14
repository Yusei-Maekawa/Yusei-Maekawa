import requests
import re

USERNAME = "Y_Maekawa"
GOAL = 1200
README_PATH = "README.md"

def get_user_info(username):
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user_info?user={username}"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception("Failed to fetch AtCoder info")
    data = res.json()
    return data.get("algorithm_rating", 0), data.get("heuristic_rating", 0)

def update_readme(algo_remain, heur_remain):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_section = (
        f'<p align="center">\n'
        f'  <strong>📈 Algorithm Goal: {GOAL} — Remaining: {algo_remain} points</strong><br>\n'
        f'  <strong>🧠 Heuristic Goal: {GOAL} — Remaining: {heur_remain} points</strong>\n'
        f'</p>'
    )

    updated = re.sub(
        r'<!-- AtCoder Rating Goal Section: Do not edit below. This will be auto-updated -->.*?<!-- End AtCoder Rating Goal Section -->',
        f'<!-- AtCoder Rating Goal Section: Do not edit below. This will be auto-updated -->\n{new_section}\n<!-- End AtCoder Rating Goal Section -->',
        content,
        flags=re.DOTALL
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    algo_rating, heur_rating = get_user_info(USERNAME)
    algo_remain = max(GOAL - algo_rating, 0)
    heur_remain = max(GOAL - heur_rating, 0)
    update_readme(algo_remain, heur_remain)
