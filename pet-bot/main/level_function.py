from bios import species as sp
import random

def add_exp(level, exp):

    evolved = False
    # check if already evolved
    if level > 10:
        evolved = True

    levelup = False 
    new_level = level + exp

    # break off the whole number and fraction
    whole = int(new_level)
    fraction = new_level - whole

    # check if level up
    if int(new_level) > int(level):
        levelup = True

    # if it didn't evolve yet and if it leveled up to 5, evolve
    if evolved is False and levelup is True:
        if int(new_level) >= 10:
            evolved = True
    # if it already evolved or not ready, do not evolve
    else:
        evolved = False

    return levelup, evolved, new_level

def level_5 (species):
    pass

def level_10 (species):
    pass

def display_level(level):

    # break off the whole number and fraction
    whole = int(level)
    fraction = level - whole

    return whole, fraction

def species_package():
    "initialize random species, level, and gender"

    species_type_list = ["common", "special", "rare", "extraordinary"]
    type_rng = random.randint(1,10)

    match type_rng:
        case x if x <= 4: species_type = species_type_list[0] # common
        case x if x <= 7: species_type = species_type_list[1] # special
        case x if x <= 9: species_type = species_type_list[2] # rare
        case x if x <= 10: species_type = species_type_list[3] # extraordinary

    # ex. common_species
    species = sp.species[f"{species_type}_species"]
    species_number = len(species)
    s = random.randint(0, species_number-1)
    specie, description = list(species.items())[s]

    evolved = sp.species["evolved_species"][specie][0]
    rarity = sp.rarity[specie]

    gender_rng = random.randint(1,2)
    match gender_rng:
        case 1: gender = "female"
        case 2: gender = "male"

    return specie, description, evolved, rarity, gender

def species_pack():
    "initialize random species, level, and gender"

    species = "frog"
    level = 0
    gender = "male"

    return species, level, gender
