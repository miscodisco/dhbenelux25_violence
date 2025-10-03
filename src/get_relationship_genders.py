import pandas as pd
import gender_guesser.detector as gender_detect
from tqdm import tqdm

from collections import Counter
from pathlib import Path

from util import read_jsonl, write_jsonl, manual_gender_dict, get_fic_fandom


def main():
    DATAPATH = Path("../../temp2.ndjson")
    OUTPATH = Path("fics_meta.ndjson")

    # load gender guesser and manual dict
    g = gender_detect.Detector()
    manual_g = manual_gender_dict()

    # load data
    df = read_jsonl(DATAPATH)

    # keeping track of unknown names
    unknown_names = []

    # saving only metadata necessary for analysis
    metadata = []

    # let's gooo
    for fic in tqdm(df):
        metadata_fic = {}
        # get the relationship tags
        relationships = fic["relationship"]

        # check if there are any slash relationships (we are not interested in platonic)
        n_slash_ships = len([ship for ship in relationships if "/" in ship])

        # if there is only 1 slash ship
        if n_slash_ships == 1:
            for ship in relationships:
                # because someone fucked up and added two slashes wihtout a name inbetween
                ship = ship.replace("//", "/")
                # find the slash ship
                if "/" in ship:
                    # get the names in the ship
                    clean_ship = ship.replace("'", "")
                    names = clean_ship.split("/")

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
                            gender = manual_g.get(first_name, "unknown")
                            if gender == "unknown":
                                # if name still unknown, add it to the list
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
        # save the metadata we need and the new genders
        metadata_fic = {
            "work_id": fic["work_id"],
            "author": fic["author"],
            "published": fic["published"],
            "fandom_label": get_fic_fandom(fic["fandom"]),
            "relationship_tags": relationships,
            "ship_genders": genders,
            "freeform_tags": fic["freeform"],
        }

        metadata.append(metadata_fic)

    # save the data
    write_jsonl(metadata, OUTPATH)

    print(Counter(unknown_names).most_common(15))


if __name__ == "__main__":
    main()
