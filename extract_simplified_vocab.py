from typing import List

from common import new_vocab_list_file, simplified_vocab_lists_dir
from utils import extract_expressions


def extract_lesson(tag_field: str) -> int:
    tag_collection = tag_field.split()
    lesson = -1
    for tag in tag_collection:
        if len(tag) == 3:  # should use regex
            lesson = int(tag[1:])
    return lesson


def simplify_vocab() -> List[List[str]]:
    simplified_collection = [[] for i in range(51)]
    with open(new_vocab_list_file) as in_f:
        for note in in_f:
            field_collection = note.split("\t")
            expression_collection = extract_expressions(field_collection[1])
            lesson = extract_lesson(field_collection[-1])
            if lesson == -1:
                continue
            simplified_collection[lesson - 1].extend(expression_collection)
    return simplified_collection


def save_simplified_vocab(simplified_collection: List[List[str]]) -> None:
    if not simplified_vocab_lists_dir.exists():
        simplified_vocab_lists_dir.mkdir()
    for lesson, simplified in enumerate(simplified_collection, 1):
        simplified_vocab_list_file = simplified_vocab_lists_dir / (
            str(lesson).zfill(2) + ".txt"
        )
        simplified_vocab_list_file.write_text("\n".join(simplified) + "\n")


def extract_simplified_vocab() -> None:
    save_simplified_vocab(simplify_vocab())


if __name__ == "__main__":
    extract_simplified_vocab()
