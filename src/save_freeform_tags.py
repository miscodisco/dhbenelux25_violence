import pandas as pd
from tqdm import tqdm

from collections import Counter

from util import read_jsonl, write_jsonl


def main():
    data = read_jsonl("fics_meta.ndjson")
    freeform_tags = []

    for fic in data:
        freeform_clean = [tag.strip().lower() for tag in fic["freeform_tags"]]
        freeform_tags.extend(freeform_clean)

    most_popular_tags = Counter(freeform_tags).most_common(1000)

    with open("most_common_tags_1000.txt", "w") as f:
        f.write(str(most_popular_tags))


if __name__ == "__main__":
    main()
