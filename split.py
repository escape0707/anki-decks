import shutil
from itertools import islice
from pathlib import Path
from typing import Iterable, cast

import pydub
import pydub.silence
from pydub.audio_segment import AudioSegment

from common import chunks_dir, input_file


def split_and_save(input_file: Path, output_dir: Path) -> None:
    soundtrack = pydub.AudioSegment.from_file(input_file)
    chuck_collection = cast(
        Iterable[AudioSegment],
        pydub.silence.split_on_silence(
            soundtrack, min_silence_len=800, silence_thresh=-50
        ),
    )

    # Skip audio chunks "daiikka" & "dango"
    for i, chunk in enumerate(islice(chuck_collection, 2, None)):
        chunk.export(output_dir / f"{i}.mp3")


if __name__ == "__main__":
    shutil.rmtree(chunks_dir)
    chunks_dir.mkdir()
    split_and_save(input_file, chunks_dir)
