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
            soundtrack, min_silence_len=800, silence_thresh=-50
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


if __name__ == "__main__":
    split_mp3()
