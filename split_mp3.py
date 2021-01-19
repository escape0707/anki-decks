import shutil
from itertools import islice
from pathlib import Path
from typing import List, cast

import pydub
import pydub.silence
from pydub.audio_segment import AudioSegment

from common import chunks_dir, input_file


def split_and_save(input_file: Path, output_dir: Path) -> None:
    soundtrack = pydub.AudioSegment.from_file(input_file)
    chuck_collection = cast(
        List[AudioSegment],
        pydub.silence.split_on_silence(
            soundtrack, min_silence_len=800, silence_thresh=-50
        ),
    )

    # Skip audio chunks "daiikka" & "dango"
    for i, chunk in enumerate(islice(chuck_collection, 2, None)):
        chunk.export(output_dir / (str(i).zfill(4) + ".mp3"))


def split_mp3() -> None:
    if chunks_dir.exists():
        shutil.rmtree(chunks_dir)
    if not chunks_dir.exists():
        chunks_dir.mkdir()
    split_and_save(input_file, chunks_dir)


if __name__ == "__main__":
    split_mp3()
