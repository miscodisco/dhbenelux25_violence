import pandas as pd

import json

from util import read_jsonl


def main():
    # load violence tags and categories 
    with open("violence_tags.json", "r") as f:
        violence_cats = json.load(f)

    # load own data and make into a dataframe
    data = read_jsonl("data/fics_meta.ndjson")
    df = pd.DataFrame(data)

    # load Julia's data and preprocess
    aglr = pd.read_csv("data/anonymized_MythFic_metadata.csv", sep=";")
    aglr["fandom_label"] = "AGLR"
    aglr = aglr.rename(columns = {"additional tags": "freeform"})
    aglr = aglr[aglr['freeform'].notna()]

    # combine the data 
    cols_for_analysis = [column for column in aglr.columns if column in df.columns]
    aglr = aglr[cols_for_analysis]

    full_df = pd.concat([df, aglr])

    # looping over the categories 
    for category in violence_cats:
        cat_tags = violence_cats[category]

        # make a list to save the counts, so we can make a column 
        temp_column = []

        for _, fic in full_df.iterrows():
            if fic["fandom_label"] != "AGLR": # my data has tags as list, so we need to make it a str
                fic_tags = str(fic["freeform"]).lower()
            elif fic["fandom_label"] == "AGLR": # julia's data has tags as a string already
                fic_tags = fic['freeform'].lower()

            # get a list of category tags that are in the current fic's tags
            fic_cat_tags = [tag for tag in cat_tags if tag in fic_tags]

            # get the number of tags for this category for this fic
            temp_column.append(len(fic_cat_tags))

        # make new column with the number of violence tags for this cateogry
        full_df["violence_" + category] = temp_column
    
    # save the data 
    full_df.to_csv("data/all_fics_meta.csv", index=False)


if __name__ == "__main__":
    main()
