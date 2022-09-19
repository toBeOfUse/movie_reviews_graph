import json
from pathlib import Path
from collections import defaultdict

reviewers: dict[str, int] = defaultdict(lambda: 0)

files = list(Path(".").glob("review_data/*.json"))
for file_path in files:
    with open(file_path, encoding="utf-8") as file:
        reviews = json.load(file)
    seen_reviewers = set()
    for review in reviews:
        if review["rating"] != -1 and review["userID"] not in seen_reviewers:
            reviewers[review["userID"]] += 1
            seen_reviewers.add(review["userID"])

review_counts: dict[int, int] = defaultdict(lambda: 0)
for review_count in reviewers.values():
    assert review_count <= 3
    review_counts[review_count] += 1


print(f"in the files [{', '.join(map(str, files))}]:")
for review_count, reviewers_with_that_count in review_counts.items():
    print(reviewers_with_that_count, "people reviewed", review_count, "of the movies")
