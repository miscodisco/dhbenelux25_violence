import pandas as pd

import json

from util import read_jsonl


def main():
    with open("violence_tags.json", "r") as f:
        violence_cats = json.load(f)

    data = read_jsonl("fics_meta.ndjson")

    for category in violence_cats:
        cat_tags = violence_cats[category]

        for fic in data:
            fic_tags = str(fic["freeform_tags"]).lower()

            fic_cat_tags = [tag for tag in cat_tags if tag in fic_tags]

            fic["violence_" + category] = len(fic_cat_tags)

    df = pd.DataFrame(data)

    df.to_csv("fics_meta.csv", index=False)


if __name__ == "__main__":
    main()
