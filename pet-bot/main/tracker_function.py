import csv
from datetime import datetime, timedelta

def intial_interact(filename, userid):
    """
    Function add initial interacts once pet is adopted.
    """

    # write to the file
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "pet_log", "fed", "fed_log", "bath", "bath_log"])
        writer.writerow({
            "userid":userid,
            "pet":0,
            "pet_log":"",
            "fed":0,
            "fed_log":"",
            "bath":0,
            "bath_log":"",
        })

def pet_interact(filename, userid):
    """
    Function keep track of pet interacts.
    """

    # add all the userids to a set to check if it exists
    userinfo = []

    # read the file to add or update
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # if the userid is found, update if update=1, otherwise, do not update and send error
            if row["userid"] == str(userid):

                pet_count = int(row["pet"])

                # for logging in the time of the first pet interact
                if pet_count == 0:
                    row["pet_log"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                # reset pet interacts if it passes 24 hours since the first interact
                now = datetime.now()
                pet_log_dt = datetime.strptime(row["pet_log"], "%Y-%m-%d %H:%M:%S.%f")
                duration = now - pet_log_dt

                if duration >= timedelta(hours=24):
                    pet_count = 0
                    row["pet_log"] = datetime.now()
                    
                # for updating number of pet interacts
                if pet_count < 3:
                    pet_count += 1
                    row["pet"] = str(pet_count)
                # reached the max number of pet interacts
                else:
                    return 0
            userinfo.append(row)

    # write to the file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "pet_log", "fed", "fed_log", "bath", "bath_log"])
        writer.writeheader()
        writer.writerows(userinfo)
    return 1 # 

def feed_interact(filename, userid):
    """
    Function keep track of feed interacts.
    """

    # add all the userids to a set to check if it exists
    userinfo = []

    # read the file to add or update
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # if the userid is found, update if update=1, otherwise, do not update and send error
            if row["userid"] == str(userid):

                fed_count = int(row["fed"])

                # for logging in the time of the first feed interact
                if fed_count == 0:
                    row["fed_log"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                # reset feed interacts if it passes 12 hours since the first interact
                now = datetime.now()
                fed_log_dt = datetime.strptime(row["fed_log"], "%Y-%m-%d %H:%M:%S.%f")
                duration = now - fed_log_dt
                if duration >= timedelta(hours=12):
                    fed_count = 0
                    row["fed_log"] = datetime.now()
                    
                # for updating number of feed interacts
                if fed_count < 1:
                    fed_count += 1
                    row["fed"] = str(fed_count)
                # reached the max number of feed interacts
                else:
                    return 0
            userinfo.append(row)

    # write to the file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "pet_log", "fed", "fed_log", "bath", "bath_log"])
        writer.writeheader()
        writer.writerows(userinfo)
    return 1 # 

def bath_interact(filename, userid):
    """
    Function keep track of bath interacts.
    """

    # add all the userids to a set to check if it exists
    userinfo = []

    # read the file to add or update
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # if the userid is found, update if update=1, otherwise, do not update and send error
            if row["userid"] == str(userid):

                bath_count = int(row["bath"])

                # for logging in the time of the first bath interact
                if bath_count == 0:
                    row["bath_log"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                # reset bath interacts if it passes 24 hours since the first interact
                now = datetime.now()
                bath_log_dt = datetime.strptime(row["bath_log"], "%Y-%m-%d %H:%M:%S.%f")
                duration = now - bath_log_dt
                if duration >= timedelta(hours=24):
                    bath_count = 0
                    row["bath_log"] = datetime.now()
                    
                # for updating number of bath interacts
                if bath_count < 1:
                    bath_count += 1
                    row["bath"] = str(bath_count)
                # reached the max number of bath interacts
                else:
                    return 0
            userinfo.append(row)

    # write to the file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "pet_log", "fed", "fed_log", "bath", "bath_log"])
        writer.writeheader()
        writer.writerows(userinfo)
    return 1 # 

def remove_interacts(filename, userid):
    filtered_info = []
    deleted = False

    # filter out all the userids that do not match the targeted userid
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # append all the unmatches to the filtered info
            if row["userid"] != str(userid):
                filtered_info.append(row)
            else:
                deleted = True
    
    if deleted:
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["userid", "pet", "pet_log", "fed", "fed_log", "bath", "bath_log"])
            writer.writeheader()
            writer.writerows(filtered_info)
        return 1 # deleted successfully
    return 0 # nothing to delete

def check_interact(filename, userid):
    # filter out all the userids that do not match the targeted userid
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # append all the unmatches to the filtered info
            if row["userid"] == str(userid):
                return row