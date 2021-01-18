import itertools
import pathlib
import shutil
from typing import Iterable, List, cast, Tuple

import pydub
import pydub.silence
from pydub.audio_segment import AudioSegment


def split_and_save(input_file: pathlib.Path, output_dir: pathlib.Path) -> None:
    soundtrack = pydub.AudioSegment.from_file(input_file)
    chuck_collection = cast(
        Iterable[AudioSegment],
        pydub.silence.split_on_silence(
            soundtrack, min_silence_len=800, silence_thresh=-50
        ),
    )

    # Skip audio chunks "daiikka" & "dango"
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


def generate_new_vocab_list() -> None:
    vocab_list_file = data_dir / "vocab_list.txt"
    with open(vocab_list_file) as in_f, open(new_vocab_list_file, "a") as out_f:


def process_mp3_collection(
    mp3_collection: Tuple[pathlib.Path, ...], processed_word_count: int
) -> int:
    processed_mp3_count = 0
    new_vocab_list_file = data_dir / "new_vocab_list.txt"
        for note in itertools.islice(in_f, processed_word_count, None):
            field_collection = note.split()
            expression_collection = extract_expressions(field_collection[0])
            for expression in expression_collection:
                if processed_mp3_count == len(mp3_collection):
                    return processed_word_count
                mp3_path = mp3_collection[processed_mp3_count]
                processed_mp3_count += 1
                new_mp3_path = mp3_path.parent / .with_name(expression)
                mp3_path.link_to(
                    new_mp3_path
                )  # order is correct, change to rename later
            audio_field = "".join(
                map(lambda x: f"[sound:{x}.mp3]", expression_collection)
            )
            new_note = "\t".join((note.rstrip(), audio_field, "\n"))
            out_f.write(new_note)
            processed_word_count += 1
    return processed_word_count


if __name__ == "__main__":
    data_dir = pathlib.Path("./data")
    input_file = next((data_dir / "input").iterdir())
    chunks_dir = data_dir / "chunks"
    # shutil.rmtree(output_dir)
    # output_dir.mkdir()
    # split_and_save(input_file, output_dir)

    generate_new_vocab_list()

    word_count = 0
    word_count_file = data_dir / "processed_word_count_cache.txt"
    if word_count_file.exists():
        word_count = int(word_count_file.read_text())
    mp3_collection = tuple(chunks_dir.iterdir())
    new_word_count = process_mp3_collection(mp3_collection, word_count)
    new_word_count_file = word_count_file.with_stem("new_" + word_count_file.stem)
    new_word_count_file.write_text(str(new_word_count))
