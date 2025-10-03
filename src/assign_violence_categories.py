import pandas as pd

from tqdm import tqdm
import json


def main():
    with open("violence_tags.json", "r") as f:
        violence_cats = json.load(f)

    df = pd.read_csv("real_9000_fics_w_genders.csv")

    for category in violence_cats:
        cat_tags = violence_cats[category]

        temp_column_list = []

        for _, fic in df.iterrows():
            # hmm currently getting all abuse incl. child abuse, do not want
            # need to ask julia what she did
            fic_tags = fic["freeform"].lower()

            fic_cat_tags = [tag for tag in cat_tags if tag in fic_tags]

            temp_column_list.append(len(fic_cat_tags))

        df["violence_" + category] = temp_column_list

    df.to_csv("real_9000_fics_w_genders_violence.csv", index=False)


if __name__ == "__main__":
    main()
