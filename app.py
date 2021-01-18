import pathlib
import shutil

import pydub
import pydub.silence

working_dir = pathlib.Path("./working")
output_dir = working_dir / "output"
shutil.rmtree(output_dir)
output_dir.mkdir()
input_file = next((working_dir / "input").iterdir())

soundtrack = pydub.AudioSegment.from_file(input_file)
chucks = pydub.silence.split_on_silence(
    soundtrack, min_silence_len=700, silence_thresh=-40, keep_silence=200
)

for i, chunk in enumerate(chucks):
    chunk.export(output_dir / f"{i}.mp3")
