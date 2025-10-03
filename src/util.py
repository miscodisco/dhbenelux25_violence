import json


def read_jsonl(path: str) -> list[dict]:
    """ """
    with open(path, "r") as jsonl_file:
        object = [json.loads(line.strip()) for line in jsonl_file]
    return object


def write_jsonl(object: list[dict], path: str) -> None:
    """ """
    with open(path, "w") as jsonl_file:
        for data_dict in object:
            # Write each dictionary as a separate line in the jsonl file
            jsonl_file.write(json.dumps(data_dict) + "\n")


def get_fic_fandom(fandom_list: list[str]) -> str:
    """
    get the clean fandom label for future analysis based on the user-generated fandom tags
    """
    LOTR_tag = "Lord of the Rings"
    HP_tag = "Harry Potter"
    PJ = "Percy Jackson"

    if any(LOTR_tag for tag in fandom_list):
        return "LOTR"

    if any(HP_tag for tag in fandom_list):
        return "HP"

    if any(PJ for tag in fandom_list):
        return "PJ"


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
        "Scorpius": "male",
        "Boromir": "male",
        "Credence": "male",
        "Celebrian": "male",
        "Nymphadora": "female",
        "Voldemort": "male",
        "Narcissa": "female",
        "Pippin": "male",
        "Thorin": "male",
        "Haldir": "male",
        "Elrohir": "male",
        "Bilbo": "male",
        "Galadriel": "female",
        "Bellatrix": "female",
    }
    return gender_dict
