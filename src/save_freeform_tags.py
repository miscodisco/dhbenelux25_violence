import pandas as pd
from tqdm import tqdm

from collections import Counter

from util import read_jsonl, write_jsonl


def main():
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

    # get ready for looping
    fandoms = ["AGLR", "HP", "PJ", "LOTR"]

    # we want the top 500 tags for each fandom, bc HP is so huge 
    for fandom in tqdm(fandoms): 
        fandom_data = full_df.loc[full_df["fandom_label"] == fandom]

        freeform_tags = []

        for _, fic in fandom_data.iterrows():
            if fandom != "AGLR":
                freeform_clean = [tag.strip().lower() for tag in fic["freeform"]]
            elif fandom == "AGLR":
                try:
                    freeform_list = fic["freeform"].split(",")
                except:
                    print(f"something up with this fic: {fic['freeform']}")
                    continue
                    
                freeform_clean = [tag.strip().lower() for tag in freeform_list]
                
            freeform_tags.extend(freeform_clean)

        most_popular_tags = Counter(freeform_tags).most_common(500)

        with open(f"tags/{fandom}_most_common_tags_500.txt", "w") as f:
            f.write(str(most_popular_tags))


if __name__ == "__main__":
    main()
