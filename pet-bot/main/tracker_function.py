import csv
from datetime import datetime, timedelta

def pet_interact(pet, pet_log):
    """
    Function keep track of pet interacts.
    """

    pet_count = pet
    flag = False

    # for logging in the time of the first pet interact
    if pet_count == 0:
        pet_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # reset pet interacts if it passes 24 hours since the first interact
    now = datetime.now()
    pet_log_dt = datetime.strptime(pet_log, "%Y-%m-%d %H:%M:%S.%f")
    duration = now - pet_log_dt

    if duration >= timedelta(hours=24):
        pet_count = 0
        pet_log = datetime.now()
        
    # for updating number of pet interacts
    if pet_count < 3:
        pet_count += 1
        flag = True
    
    return pet_count, pet_log, flag

def feed_interact(fed, fed_log):
    """
    Function keep track of feed interacts.
    """

    fed_count = fed
    flag = False

    # for logging in the time of the first feed interact
    if fed_count == 0:
        fed_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # reset feed interacts if it passes 12 hours since the first interact
    now = datetime.now()
    fed_log_dt = datetime.strptime(fed_log, "%Y-%m-%d %H:%M:%S.%f")
    duration = now - fed_log_dt
    if duration >= timedelta(hours=12):
        fed_count = 0
        fed_log = datetime.now()
        
    # for updating number of feed interacts
    if fed_count < 1:
        fed_count += 1
        flag = True

    return fed_count, fed_log, flag

def bath_interact(bath, bath_log):
    """
    Function keep track of bath interacts.
    """

    bath_count = bath
    flag = False

    # for logging in the time of the first bath interact
    if bath_count == 0:
        bath_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # reset bath interacts if it passes 24 hours since the first interact
    now = datetime.now()
    bath_log_dt = datetime.strptime(bath_log, "%Y-%m-%d %H:%M:%S.%f")
    duration = now - bath_log_dt
    if duration >= timedelta(hours=24):
        bath_count = 0
        bath_log = datetime.now()
        
    # for updating number of bath interacts
    if bath_count < 1:
        bath_count += 1
        flag = True
    
    return bath_count, bath_log, flag
