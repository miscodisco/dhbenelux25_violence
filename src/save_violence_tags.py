import pandas as pd

from collections import Counter
from tqdm import tqdm


def main():
    df = pd.read_csv("real_9000_fics_w_genders.csv")

    freeform_tags = []

    for _, fic in df.iterrows():
        fic_freeform = fic["freeform"][1:-1].replace("'", "")

        fic_freeform_list = [tag.strip().lower() for tag in fic_freeform.split(", ")]

        freeform_tags.extend(fic_freeform_list)

    most_popular_tags = Counter(freeform_tags).most_common(500)

    with open("most_common_tags_500.txt", "w") as f:
        f.write(str(most_popular_tags))


if __name__ == "__main__":
    main()
