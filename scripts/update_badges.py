# scripts/update_badges.py
import requests
import re

USERNAME = "Y_Maekawa"
README_PATH = "README.md"

def get_rating(kind: str):
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/info?user={USERNAME}"
    res = requests.get(url)
    data = res.json()
    if kind == "algorithm":
        return data.get("algorithm_rating", "N/A")
    elif kind == "heuristic":
        return data.get("heuristic_rating", "N/A")
    return "N/A"

def replace_badges(readme):
    algo_rating = get_rating("algorithm")
    heur_rating = get_rating("heuristic")

    readme = re.sub(
        r"!\[Algorithm Rating\]\(.*?\)",
        f"![Algorithm Rating](https://img.shields.io/badge/Algorithm-{algo_rating}-blue)",
        readme
    )
    readme = re.sub(
        r"!\[Heuristic Rating\]\(.*?\)",
        f"![Heuristic Rating](https://img.shields.io/badge/Heuristic-{heur_rating}-purple)",
        readme
    )
    return readme

if __name__ == "__main__":
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()
    updated = replace_badges(content)
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
