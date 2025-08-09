import csv

def intial_interact(filename, userid):
    """
    Function add initial interacts once pet is adopted.
    """

    # write to the file
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "fed", "bath"])
        writer.writerow({
            "userid":userid,
            "pet":0,
            "fed":0,
            "bath":0
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
                # for updating information of the pet
                pet_count = int(row["pet"])
                if pet_count < 3:
                    pet_count += 1
                    row["pet"] = str(pet_count)
                # reached the max number of pet interacts
                else:
                    return 0
            userinfo.append(row)

    # write to the file
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["userid", "pet", "fed", "bath"])
        writer.writeheader()
        writer.writerows(userinfo)
    return 1 # 