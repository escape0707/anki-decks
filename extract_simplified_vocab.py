import re
from typing import Iterator, List, Tuple

from common import vocab_list_file, revised_lesson_count, simplified_vocab_lists_dir
from utils import extract_expressions


def extract_lesson(tag_field: str) -> Tuple[Iterator[int], Iterator[int]]:
    lesson_collection = map(int, re.findall(r"L(\d{2})(?!U)", tag_field))
    lesson_u_collection = map(int, re.findall(r"L(\d{2})U", tag_field))
    assert lesson_collection or lesson_u_collection
    return lesson_collection, lesson_u_collection


def simplify_vocab() -> Tuple[List[List[str]], List[List[str]]]:
    simplified_collection = [[] for i in range(51)]
    extra_collection = [[] for i in range(51)]
    with open(vocab_list_file) as in_f:
        for note in in_f:
            field_collection = note.split("\t")
            expression_collection = extract_expressions(field_collection[0])
            lesson_collection, lesson_u_collection = extract_lesson(
                field_collection[-1]
            )
            for lesson in lesson_collection:
                simplified_collection[lesson - 1].extend(expression_collection)
            for lesson_u in lesson_u_collection:
                extra_collection[lesson_u - 1].extend(expression_collection)
    return simplified_collection, extra_collection


# TODO: the ugliest code is here
def save_simplified_vocab(
    simplified_collection: List[List[str]], extra_collection: List[List[str]]
) -> None:
    if not simplified_vocab_lists_dir.exists():
        simplified_vocab_lists_dir.mkdir()
    for lesson, simplified in enumerate(simplified_collection, 1):
        if lesson <= revised_lesson_count:
            continue
        simplified_vocab_list_file = simplified_vocab_lists_dir / (
            str(lesson).zfill(2) + ".txt"
        )
        simplified_vocab_list_file.write_text("\n".join(simplified) + "\n")
    for lesson_u, extra in enumerate(extra_collection, 1):
        simplified_vocab_list_file = simplified_vocab_lists_dir / (
            str(lesson_u).zfill(2) + "U.txt"
        )
        simplified_vocab_list_file.write_text("\n".join(extra) + "\n")


def extract_simplified_vocab() -> None:
    save_simplified_vocab(*simplify_vocab())


if __name__ == "__main__":
    extract_simplified_vocab()
