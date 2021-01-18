import itertools
import pathlib
import shutil
from typing import List

import pydub
import pydub.silence

working_dir = pathlib.Path("./working")
output_dir = working_dir / "output"
shutil.rmtree(output_dir)
output_dir.mkdir()
input_file = next((working_dir / "input").iterdir())

word_count_file = working_dir / "processed_word_count_cache.txt"
word_count = int(word_count_file.read_text())


def split_and_save(input_file: pathlib.Path, output_dir: pathlib.Path) -> None:
    soundtrack = pydub.AudioSegment.from_file(input_file)
    chuck_collection = pydub.silence.split_on_silence(
        soundtrack, min_silence_len=800, silence_thresh=-50
    )

    for i, chunk in enumerate(itertools.islice(chuck_collection, 2, None)):
        chunk.export(output_dir / f"{i}.mp3")


def extract_expressions(expression_field: str) -> List[str]:
    expression_collection = []
    word_start = 0
    word_end = expression_field.find("（")
    while True:
        if word_end == -1:
            word_end = len(expression_field)
        expression_collection.append(expression_field[word_start:word_end])
        word_start = expression_field.find("（", word_end + 1)
        if word_start == -1:
            break
        word_end = expression_field.find("）", word_start)
    return expression_collection


def process_mp3_collection() -> None:
    vocab_list_file = working_dir / "vocab_list.txt"
    with open(vocab_list_file) as f:
        map(pair_mp3_with_word, f)
