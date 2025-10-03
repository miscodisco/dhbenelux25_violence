import pandas as pd
import gender_guesser.detector as gender_detect

from collections import Counter

from util import read_jsonl, write_jsonl


def manual_gender_dict():
    gender_dict = {
        "Draco": "male",
        "Hermione": "female",
        "Legolas": "male",
        "Sirius": "male",
        "Severus": "male",
        "Aragorn": "male",
        "Gimli": "male",
        "Glorfindel": "male",
        "Erestor": "male",
        "Faramir": "male",
        "Eowyn": "female",
        "Thranduil": "male",
        "Albus": "male",
        "Eomer": "male",
    }
    return gender_dict


def main():
    # load gender guesser and manual dict
    g = gender_detect.Detector()
    manual_g = manual_gender_dict()

    # load data
    df = read_jsonl("../../temp2.json")

    genders_column = []
    unknown_names = []

    for _, fic in df.iterrows():
        # get the relationship tags
        relationships = fic["relationship"]

        # make it a list
        relationship_list = relationships[1:-1].split(",")
        # check if there are any slash relationships (we are not interested in platonic)
        n_slash_ships = relationships.count("/")

        # if there is only 1 slash ship
        if n_slash_ships == 1:
            for ship in relationship_list:
                # find the slash ship
                if "/" in ship:
                    # get the names in the ship
                    clean_names = ship.replace("'", "")
                    names = clean_names.split("/")

                    # save the genders of the names in the ship
                    genders_list = []
                    # for each person in the ship
                    for name in names:
                        # find the first name
                        first_name = name.split(" ")[0]

                        # sometimes there's a space before the name, if that is the case, select the second item
                        if first_name == "":
                            first_name = name.split(" ")[1]
                        # sometimes people write "Original [GENDER] Character" - so we use that gender and move on
                        if first_name == "Original":
                            gender = name.split(" ")[1].lower()
                            genders_list.append(gender)
                            continue

                        # then we try to use the gender guesser
                        gender = g.get_gender(first_name)

                        # if it's mostly, we just trust
                        if "mostly" in gender:
                            gender = gender[7:]

                        # if it's unknown, we use the manual gender dict for the most common names
                        if gender == "unknown":
                            # unknown_names.append(first_name)
                            gender = manual_g.get(first_name, "unknown")
                            if gender == "unknown":
                                # running a second round for the big data
                                unknown_names.append(first_name)

                        genders_list.append(gender)

                    # save it as a string instead of list
                    genders = "_".join(genders_list)

        # if there are no slash ship, note that
        elif n_slash_ships == 0:
            genders = "no_ships"
        # more than one slash ship is called multiple
        elif n_slash_ships > 1:
            genders = "multiple"
        # save the genders
        genders_column.append(genders)

    df["ship_genders"] = genders_column

    print(Counter(unknown_names).most_common(15))

    # df.to_csv("real_9000_fics_w_genders.csv", index=False)


if __name__ == "__main__":
    main()
