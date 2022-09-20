import json
from pathlib import Path
from collections import defaultdict
from itertools import combinations

# keys are reviewer ids, values are how many movies they reviewed
reviewers: dict[str, int] = defaultdict(lambda: 0)
# keys are movie data file names, values are the set of userIDs for people who
# reviewed that movie
reviewers_by_movie: dict[str, set[str]] = defaultdict(set)
# keys are a (userID, movie data file name) tuple, values are the rating that
# user gave that movie out of 10
scores: dict[tuple[str, str], int] = {}

files = list(str(x) for x in Path(".").glob("review_data/*.json"))
for file_path in files:
    with open(file_path, encoding="utf-8") as file:
        reviews = json.load(file)
    # keeping track of what reviewers have reviewed this movie so if they have a
    # double review we can skip it... kind of weird
    seen_reviewers = set()
    for review in reviews:
        if review["rating"] != -1 and review["userID"] not in seen_reviewers:
            reviewers[review["userID"]] += 1
            reviewers_by_movie[file_path].add(review["userID"])
            scores[(review["userID"], file_path)] = review["rating"]
            seen_reviewers.add(review["userID"])

# each table row is a movie data file name, another movie data file name, the
# average difference between same-author reviews of the two movies, and the
# number of same-author reviews of the two movies
combination_row = []
for combo in combinations(files, 2):
    reviewers_of_both = reviewers_by_movie[combo[0]] & reviewers_by_movie[combo[1]]
    accum = 0
    for reviewer in reviewers_of_both:
        accum += abs(scores[(reviewer, combo[0])]-scores[(reviewer, combo[1])])
    combination_row.append(
        (
            Path(combo[0]).stem, 
            Path(combo[1]).stem, 
            round(accum/len(reviewers_of_both), 4), 
            len(reviewers_of_both)
        )
    )
combination_row.sort(key=lambda x: x[2])
row_format = "{:<30}"*4
print("average difference between movie reviews made by the same person for each pair of movies:")
print(row_format.format(*["movie 1","movie 2","review difference","sample size"]))
print("-"*(30*4))
for combo in combination_row:
    print(row_format.format(*combo))


# keys are quantities of reviews, values are how many reviewers made that quantity of reviews
review_counts: dict[int, int] = defaultdict(lambda: 0)
for review_count in reviewers.values():
    assert review_count <= len(files)
    review_counts[review_count] += 1

print(f"in the files [{', '.join(map(str, files))}]:")
for review_count, reviewers_with_that_count in sorted(
    review_counts.items(), key=lambda x: x[0], reverse=True
):
    print(
        f"{reviewers_with_that_count} people reviewed "
        f"{'all ' if review_count==len(files) else ''}{review_count} of the movies"
    )
