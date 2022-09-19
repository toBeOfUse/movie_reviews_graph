import json

with open("review_data/manofsteel.json", encoding="utf-8") as steel_file:
    steel_reviews = json.load(steel_file)
steel_reviewers = set(review["userID"] for review in steel_reviews if review["rating"] != -1)

with open("review_data/ironman.json", encoding="utf-8") as iron_file:
    iron_reviews = json.load(iron_file)
iron_reviewers = set(review["userID"] for review in iron_reviews if review["rating"] != -1)

print(f"we have {len(steel_reviewers)} people who reviewed 'man of steel', "
    f"{len(iron_reviewers)} people who reviewed 'iron man', "
    f"and {len(steel_reviewers & iron_reviewers)} people who reviewed both."    
)
