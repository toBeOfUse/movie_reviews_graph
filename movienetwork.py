import json
from pathlib import Path
from collections import defaultdict
from itertools import combinations

import networkx as nx

# IMPORT THESE:

movie_names = []
"""list of movie names, currently taken from the names of the files in the
review_data folder"""

reviewers = defaultdict(lambda: 0)
"keys are reviewer ids, values are how many movies they reviewed"

reviewers_by_movie = defaultdict(set)
"""keys are movie data file names, values are the set of userIDs for people who
reviewed that movie"""

scores = {}
"""keys are a (userID, movie data file name) tuple, values are the rating that
user gave that movie out of 10"""

total_review_count = 0

network = nx.Graph()
"""NetworkX Graph object with movie file names as nodes and weighted edges
between them; the weights are 1/(the average distance between reviews)"""

combination_row = []
"""each table row is a movie data file name, another movie data file name, the
average difference between same-author reviews of the two movies, and the
number of same-author reviews of the two movies"""


files = list(Path(".").glob("movie_data/*.json"))
movie_names = [f.stem for f in files]
movie_attrs = {}
for file_path in files:
    with open(file_path, encoding="utf-8") as file:
        movie = json.load(file)
    reviews = movie["reviews"]
    del movie["reviews"]
    movie_attrs[file_path.stem] = movie
    network.add_node(movie["title"], **movie)
    # keeping track of what reviewers have reviewed this movie so if they have a
    # double review we can skip it... kind of weird
    seen_reviewers = set()
    for review in reviews:
        if review["rating"] != -1 and review["userID"] not in seen_reviewers:
            total_review_count += 1
            reviewers[review["userID"]] += 1
            reviewers_by_movie[file_path.stem].add(review["userID"])
            scores[(review["userID"], file_path.stem)] = review["rating"]
            seen_reviewers.add(review["userID"])

for combo in combinations(map(lambda x: x.stem, files), 2):
    reviewers_of_both = reviewers_by_movie[combo[0]] & reviewers_by_movie[combo[1]]
    accum = 0
    for reviewer in reviewers_of_both:
        accum += abs(scores[(reviewer, combo[0])]-scores[(reviewer, combo[1])])
    avg_distance = accum/len(reviewers_of_both)
    combination_row.append(
        (
            *combo,
            round(avg_distance, 4), 
            len(reviewers_of_both)
        )
    )
    network.add_edge(
        movie_attrs[combo[0]]["title"],
        movie_attrs[combo[1]]["title"],
        weight = 1/avg_distance
    )

combination_row.sort(key=lambda x: x[2])

review_counts = defaultdict(lambda: 0)
"keys are quantities of reviews, values are how many reviewers made that quantity of reviews"
for review_count in reviewers.values():
    assert review_count <= len(files)
    review_counts[review_count] += 1

if __name__ == "__main__":
    row_format = "{:<30}"*4
    print("average difference between movie reviews made by the same person for each pair of movies:")
    print(row_format.format(*["movie 1","movie 2","review difference","sample size"]))
    print("-"*(30*4))
    for combo in combination_row:
        print(row_format.format(*combo))

    print(f"in the files [{', '.join(map(lambda x: x.stem, files))}]:")
    for review_count, reviewers_with_that_count in sorted(
        review_counts.items(), key=lambda x: x[0], reverse=True
    ):
        print(
            f"{reviewers_with_that_count} people reviewed "
            f"{'all ' if review_count==len(files) else ''}{review_count} of the movies"
        )
    print(f"{total_review_count} reviews total")
    print("network object exists:", network)
