from bios import species as sp

def add_exp(level, exp):

    levelup = False 

    new_level = level + exp

    # break off the whole number and fraction
    whole = int(new_level)
    fraction = new_level - whole

    # check if level up
    if int(new_level) > int(level):
        levelup = True

    return levelup, new_level

def level_5 (species):
    pass

def level_10 (species):
    pass

def display_level(level):

    # break off the whole number and fraction
    whole = int(level)
    fraction = level - whole

    return whole, fraction

def species_pack():
    "initialize random species, level, and gender"

    species = "frog"
    level = 0
    gender = "male"

    return species, level, gender

