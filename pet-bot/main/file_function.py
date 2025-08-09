import csv

def check_userinfo(filename, userid):
    """
    Function to check if the user info exists.
    Return true if it exists.
    """

    # add all the userids to a set to check if it exists
    userinfo = []

    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # has a pet
            if row["userid"] == str(userid):
                return True
            # has no pet

    return False

def add_userinfo(filename, userid, pet_name, date_adopted, hearts_status, update:int):
    """
    Function to add or update user information.
    Return true if it adds or updates.
    """

    # add all the userids to a set to check if it exists
    userinfo = []
    updated = False

    # read the file to add or update
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # if the userid is found, update if update=1, otherwise, do not update and send error
            if row["userid"] == userid:
                # for updating information of the pet
                if update == 1:
                    row = {"userid":userid, "pet_name":pet_name, "date_adopted":date_adopted, "hearts_status":hearts_status}
                    updated = True
                # if pet already exists when trying to add a pet
                elif update == 0:
                    return 0
            userinfo.append(row)

        # adding new user and information
        if not updated and update == 0:
            row = {"userid":userid, "pet_name":pet_name, "date_adopted":date_adopted, "hearts_status":hearts_status}
            userinfo.append(row)

    # write to the file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet_name", "date_adopted", "hearts_status"])
        writer.writeheader()
        writer.writerows(userinfo)
    return 1 # added successfully

def remove_userinfo(filename, userid):
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
            writer = csv.DictWriter(file, fieldnames=["userid", "pet_name", "date_adopted", "hearts_status"])
            writer.writeheader()
            writer.writerows(filtered_info)
        return 1 # deleted successfully
    return 0 # nothing to delete

def retrieve_info(filename, userid):
    """
    Retrieve only the specified information.
    """
    # user = {}
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # append all the unmatches to the filtered info
            if row["userid"] == str(userid):
                user = row
    
    return user
    