import re
import shutil
from pathlib import Path
from typing import List, cast

import pydub
import pydub.silence
from pydub.audio_segment import AudioSegment

from common import chunks_dir, input_dir


def split_and_save(input_file: Path, output_dir: Path) -> None:
    soundtrack = pydub.AudioSegment.from_file(input_file)
    chuck_collection = cast(
        List[AudioSegment],
        pydub.silence.split_on_silence(
            soundtrack, min_silence_len=800, silence_thresh=-55
        ),
    )

    # Skip audio chunks "daiikka" & "dango"
    for i, chunk in enumerate(chuck_collection):
        chunk.export(output_dir / (str(i).zfill(4) + ".mp3"))


def split_mp3() -> None:
    # if chunks_dir.exists():
    #     shutil.rmtree(chunks_dir)
    if not chunks_dir.exists():
        chunks_dir.mkdir()
    for lesson, input_file in enumerate(input_dir.iterdir(), 1):
        lesson_dir = chunks_dir / str(lesson).zfill(2)
        if lesson_dir.exists():
            continue
            shutil.rmtree(lesson_dir)
        if not lesson_dir.exists():
            lesson_dir.mkdir()
        split_and_save(input_file, lesson_dir)


def extract_lesson_no_and_rename() -> None:
    renamed_dir = input_dir.parent / "input2"
    if renamed_dir.exists():
        shutil.rmtree(renamed_dir)
    if not renamed_dir.exists():
        renamed_dir.mkdir()
    for input_file in input_dir.iterdir():
        lesson_no = re.search(r"\d+", input_file.stem).group()
        input_file.link_to(renamed_dir / f"{lesson_no:0>2}.m4a")


if __name__ == "__main__":
    split_mp3()
