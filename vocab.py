import itertools
import pathlib
import shutil
from typing import List, Tuple

from common import (
    pronunciation_dir,
    chunks_dir,
    lesson,
    new_vocab_lists_dir,
    new_word_count_file,
    vocab_list_file,
    word_count_file,
)


def extract_expressions(expression_field: str) -> List[str]:
    expression_collection = []
    word_start = 0
    word_end = expression_field.find("（")
    while True:
        if word_end == -1:
            word_end = len(expression_field)
        expression_collection.append(expression_field[word_start:word_end])
        word_start = expression_field.find("（", word_end)
        if word_start == -1:
            break
        word_start += 1
        word_end = expression_field.find("）", word_start)
    return expression_collection


def read_processed_word_count() -> int:
    word_count = 0
    if word_count_file.exists():
        word_count = int(word_count_file.read_text())
    return word_count


def save_processed_word_count(new_count: int) -> None:
    new_word_count_file.write_text(str(new_count))


def generate_new_vocab_list() -> List[str]:
    if not new_vocab_lists_dir.exists():
        new_vocab_lists_dir.mkdir()
    new_vocab_list_file = new_vocab_lists_dir / (lesson + "単語.txt")
    with open(vocab_list_file) as in_f, open(new_vocab_list_file, "w") as out_f:
        new_mp3_name_collection = []
        processed_word_count = read_processed_word_count()
        lesson_tag = None
        for note in itertools.islice(in_f, processed_word_count, None):
            field_collection = note.split("\t")
            tag_field = field_collection.pop()
            curr_lesson_tag = tag_field.split()[0]
            if lesson_tag is None:
                lesson_tag = [curr_lesson_tag, curr_lesson_tag + "U"]
            elif curr_lesson_tag not in lesson_tag:
                break
            expression_collection = extract_expressions(field_collection[0])
            for expression in expression_collection:
                new_mp3_name_collection.append(expression + ".mp3")
            index_field = str(processed_word_count + 1)
            audio_field = "".join(
                map(lambda x: f"[sound:{x}.mp3]", expression_collection)
            )
            new_note = "\t".join(
                [index_field] + field_collection + [audio_field, tag_field]
            )
            out_f.write(new_note + "\n")
            processed_word_count += 1
    save_processed_word_count(processed_word_count)
    return new_mp3_name_collection


def rename_mp3_collection(
    mp3_collection: Tuple[pathlib.Path, ...], new_mp3_name_collection: List[str]
) -> None:
    ## TODO
    if pronunciation_dir.exists():
        shutil.rmtree(pronunciation_dir)
    ## TODO
    if not pronunciation_dir.exists():
        pronunciation_dir.mkdir()
    for mp3_path, new_mp3_name in zip(mp3_collection, new_mp3_name_collection):
        new_mp3_path = pronunciation_dir / new_mp3_name
        mp3_path.link_to(new_mp3_path)  # order is correct, change to rename later


if __name__ == "__main__":
    mp3_collection = tuple(chunks_dir.iterdir())
    new_mp3_name_collection_collection = generate_new_vocab_list(len(mp3_collection))
    rename_mp3_collection(mp3_collection, new_mp3_name_collection_collection)