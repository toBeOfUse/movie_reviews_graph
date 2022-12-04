###############################################################################################################

    # This script uses the omdbapi.com developer api to retrieve and return movie data 
    # Author: Antonio Shelton-McGaha
    # Authored on: 11/20/2022

###############################################################################################################

###############################################################################################################
    # ADD THE LINE BELOW TO THE TOP OF A FILE TO USE THE 'get_new_attributes(title)' FUNCTION # 

    ############## from new_attributes import get_new_attributes ##############

    # get_new_attributes(title) takes a movie title as a string as an argument and returns a dictionary of data for that movie #
###############################################################################################################

import requests
import json

def get_new_attributes(title):
    key = 'xxxxxxxxxxx'
    url = f'https://www.omdbapi.com/?t={title}&apikey={key}'

    ############## get overall data ##############
    try:
        data = requests.get(url)
        data = data.json()
    except:
        error = {"error": "An error occurred when fetching data from API. Invalid title or apikey - item not found"}
        return error
    ##############################################

    ############## get title ##############
    try:
        movie = data["Title"]
    except:
        movie = 'no title available'
    ##############################################

    ################## get genres #################
    try:
        genres = [genre.strip() for genre in data["Genre"].split(",")]
        
    except:
        genres = 'no genres available'
    ##############################################

    ################## get actors #################
    try:
        actors = [actor.strip() for actor in data["Actors"].split(",")]
    except:
        actors = 'no actors available'
    ##############################################

    ############## get director ##############
    try:
        director = data["Director"]
    except:
        director = 'no director available'
    ##############################################

    ################ get year ################
    try:
        year = int(data["Year"])
    except:
        year = 'no year available'
    ##############################################

    return {'title':movie, 'genres':genres, 'actors':actors, 'director':director, 'year':year}

################################################################################################################
# UNCOMMENT & ADD THE BLOCK OF CODE BELOW TO A FILE TO GET A LIST OF DATA FOR EACH MOVIE IN THE 'movies' LIST #

movies = ['avengers', 'batman', 'captain_america_the_first_avenger', 'captain_america', 'dark_knight', 'deadpool', 'iron_man', 'logan', 'man_of_steel', 'superman']
data = []
for movie in movies:
    movie_attributes = get_new_attributes(movie)
    data.append(movie_attributes)
    with open(f"review_data/{movie}.json", encoding="utf-8") as review_file:
        movie_attributes["reviews"]  = json.load(review_file)
    with open(f"movie_data/{movie}.json", mode="w+", encoding="utf-8") as movie_file:
        json.dump(movie_attributes, movie_file)
      
print(data)

################################################################################################################